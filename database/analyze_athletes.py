"""
Analyse et traitement des données des athlètes olympiques
Source: MySQL AlwaysData - Données réelles
"""

import pymysql
from dotenv import load_dotenv
import os
import json
import pandas as pd
from collections import Counter

load_dotenv()

def get_connection():
    """Connexion à MySQL AlwaysData"""
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD").strip('"'),
        database=os.getenv("DB_DATABASE"),
        port=int(os.getenv("DB_PORT", 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

def analyze_athletes():
    """Analyse complète des athlètes"""
    print("\n" + "="*60)
    print("  ANALYSE DES ATHLETES OLYMPIQUES")
    print("="*60)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Statistiques générales
    print("\n[STATISTIQUES GENERALES]")
    print("-" * 60)
    
    cursor.execute("""
        SELECT COUNT(DISTINCT athlete_full_name) as total
        FROM medals
        WHERE athlete_full_name IS NOT NULL
    """)
    total_athletes = cursor.fetchone()['total']
    print(f"Total athletes medailles: {total_athletes:,}")
    
    # 2. Top 10 athlètes de tous les temps
    print("\n[TOP 10 ATHLETES - Total medailles]")
    print("-" * 60)
    
    cursor.execute("""
        SELECT 
            athlete_full_name,
            country_name,
            COUNT(*) as total_medals,
            SUM(CASE WHEN medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold,
            SUM(CASE WHEN medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver,
            SUM(CASE WHEN medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze
        FROM medals
        WHERE athlete_full_name IS NOT NULL
        GROUP BY athlete_full_name, country_name
        ORDER BY total_medals DESC, gold DESC
        LIMIT 10
    """)
    
    top_athletes = cursor.fetchall()
    for i, athlete in enumerate(top_athletes, 1):
        gold = int(athlete['gold']) if athlete['gold'] else 0
        silver = int(athlete['silver']) if athlete['silver'] else 0
        bronze = int(athlete['bronze']) if athlete['bronze'] else 0
        total = int(athlete['total_medals']) if athlete['total_medals'] else 0
        print(f"{i:2d}. {athlete['athlete_full_name']:<30} ({athlete['country_name']:<20})")
        print(f"    Total: {total:2d} | Gold:{gold:2d} Silver:{silver:2d} Bronze:{bronze:2d}")
    
    # 3. Légendes olympiques (5+ médailles d'or)
    print("\n[LEGENDES OLYMPIQUES - 5+ medailles d'or]")
    print("-" * 60)
    
    cursor.execute("""
        SELECT 
            athlete_full_name,
            country_name,
            SUM(CASE WHEN medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold,
            COUNT(*) as total
        FROM medals
        WHERE athlete_full_name IS NOT NULL
        GROUP BY athlete_full_name, country_name
        HAVING gold >= 5
        ORDER BY gold DESC
        LIMIT 20
    """)
    
    legends = cursor.fetchall()
    print(f"Nombre de legendes: {len(legends)}")
    for i, legend in enumerate(legends[:10], 1):
        print(f"{i:2d}. {legend['athlete_full_name']:<30} "
              f"({legend['country_name']:<20}) - {legend['gold']} Gold / {legend['total']} total")
    
    # 4. Analyse par sport
    print("\n[TOP 5 SPORTS PAR NOMBRE D'ATHLETES]")
    print("-" * 60)
    
    cursor.execute("""
        SELECT 
            discipline_title as sport,
            COUNT(DISTINCT athlete_full_name) as athletes
        FROM medals
        WHERE athlete_full_name IS NOT NULL
        AND discipline_title IS NOT NULL
        GROUP BY discipline_title
        ORDER BY athletes DESC
        LIMIT 5
    """)
    
    sports = cursor.fetchall()
    for i, sport in enumerate(sports, 1):
        print(f"{i}. {sport['sport']:<30} - {sport['athletes']:,} athletes")
    
    # 5. Athlètes par pays
    print("\n[TOP 10 PAYS PAR NOMBRE D'ATHLETES MEDAILLES]")
    print("-" * 60)
    
    cursor.execute("""
        SELECT 
            country_name,
            country_code,
            COUNT(DISTINCT athlete_full_name) as athletes,
            COUNT(*) as total_medals
        FROM medals
        WHERE athlete_full_name IS NOT NULL
        GROUP BY country_name, country_code
        ORDER BY athletes DESC
        LIMIT 10
    """)
    
    countries = cursor.fetchall()
    for i, country in enumerate(countries, 1):
        print(f"{i:2d}. {country['country_name']:<25} - "
              f"{country['athletes']:,} athletes / {country['total_medals']:,} medailles")
    
    # 6. Athlètes multi-sports
    print("\n[ATHLETES POLYVALENTS - Medailles dans 2+ sports]")
    print("-" * 60)
    
    cursor.execute("""
        SELECT 
            athlete_full_name,
            country_name,
            COUNT(DISTINCT discipline_title) as sports_count,
            GROUP_CONCAT(DISTINCT discipline_title) as sports,
            COUNT(*) as total_medals
        FROM medals
        WHERE athlete_full_name IS NOT NULL
        AND discipline_title IS NOT NULL
        GROUP BY athlete_full_name, country_name
        HAVING sports_count >= 2
        ORDER BY sports_count DESC, total_medals DESC
        LIMIT 10
    """)
    
    multi_sport = cursor.fetchall()
    for i, athlete in enumerate(multi_sport, 1):
        sports_list = athlete['sports'][:100] + "..." if len(athlete['sports']) > 100 else athlete['sports']
        print(f"{i:2d}. {athlete['athlete_full_name']:<30}")
        print(f"    {athlete['sports_count']} sports | {athlete['total_medals']} medailles")
        print(f"    Sports: {sports_list}")
    
    # 7. Générer JSON pour l'API
    print("\n[GENERATION DES DONNEES JSON]")
    print("-" * 60)
    
    # Top athletes JSON
    cursor.execute("""
        SELECT 
            athlete_full_name as name,
            country_name as country,
            country_code,
            COUNT(*) as total_medals,
            SUM(CASE WHEN medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold,
            SUM(CASE WHEN medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver,
            SUM(CASE WHEN medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze
        FROM medals
        WHERE athlete_full_name IS NOT NULL
        GROUP BY athlete_full_name, country_name, country_code
        ORDER BY total_medals DESC
        LIMIT 100
    """)
    top_100_raw = cursor.fetchall()
    
    # Convert Decimal to int
    top_100 = []
    for athlete in top_100_raw:
        top_100.append({
            'name': athlete['name'],
            'country': athlete['country'],
            'country_code': athlete['country_code'],
            'total_medals': int(athlete['total_medals']) if athlete['total_medals'] else 0,
            'gold': int(athlete['gold']) if athlete['gold'] else 0,
            'silver': int(athlete['silver']) if athlete['silver'] else 0,
            'bronze': int(athlete['bronze']) if athlete['bronze'] else 0
        })
    
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/top_athletes.json', 'w', encoding='utf-8') as f:
        json.dump(top_100, f, indent=2, ensure_ascii=False)
    print(f"OK top_athletes.json - {len(top_100)} athletes")
    
    # Legends JSON
    cursor.execute("""
        SELECT 
            athlete_full_name as name,
            country_name as country,
            country_code,
            SUM(CASE WHEN medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold,
            SUM(CASE WHEN medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver,
            SUM(CASE WHEN medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze,
            COUNT(*) as total_medals
        FROM medals
        WHERE athlete_full_name IS NOT NULL
        GROUP BY athlete_full_name, country_name, country_code
        HAVING gold >= 5
        ORDER BY gold DESC, total_medals DESC
    """)
    legends_raw = cursor.fetchall()
    
    # Convert Decimal to int
    legends_data = []
    for legend in legends_raw:
        legends_data.append({
            'name': legend['name'],
            'country': legend['country'],
            'country_code': legend['country_code'],
            'gold': int(legend['gold']) if legend['gold'] else 0,
            'silver': int(legend['silver']) if legend['silver'] else 0,
            'bronze': int(legend['bronze']) if legend['bronze'] else 0,
            'total_medals': int(legend['total_medals']) if legend['total_medals'] else 0
        })
    
    with open(f'{output_dir}/olympic_legends.json', 'w', encoding='utf-8') as f:
        json.dump(legends_data, f, indent=2, ensure_ascii=False)
    print(f"OK olympic_legends.json - {len(legends_data)} legendes")
    
    conn.close()
    
    print("\n" + "="*60)
    print("  ANALYSE TERMINEE")
    print("="*60 + "\n")
    
    return {
        'total_athletes': total_athletes,
        'legends_count': len(legends),
        'top_10': top_athletes
    }

def get_athlete_profile(athlete_name):
    """Profil détaillé d'un athlète"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print(f"\n[PROFIL: {athlete_name}]")
    print("="*60)
    
    # Médailles
    cursor.execute("""
        SELECT 
            medal_type,
            discipline_title,
            event_title,
            slug_game
        FROM medals
        WHERE athlete_full_name = %s
        ORDER BY slug_game
    """, (athlete_name,))
    
    medals = cursor.fetchall()
    
    if not medals:
        print("X Athlete non trouve")
        conn.close()
        return None
    
    # Statistiques
    gold = sum(1 for m in medals if m['medal_type'] == 'GOLD')
    silver = sum(1 for m in medals if m['medal_type'] == 'SILVER')
    bronze = sum(1 for m in medals if m['medal_type'] == 'BRONZE')
    
    print(f"Total medailles: {len(medals)}")
    print(f"Gold: {gold} | Silver: {silver} | Bronze: {bronze}")
    
    # Sports
    sports = set(m['discipline_title'] for m in medals if m['discipline_title'])
    print(f"\nSports ({len(sports)}): {', '.join(sports)}")
    
    # Jeux Olympiques
    games = set(m['slug_game'] for m in medals if m['slug_game'])
    print(f"Participations: {len(games)} Jeux Olympiques")
    
    conn.close()
    
    return {
        'name': athlete_name,
        'total_medals': len(medals),
        'gold': gold,
        'silver': silver,
        'bronze': bronze,
        'sports': list(sports),
        'olympics_count': len(games)
    }

if __name__ == "__main__":
    # Analyse complète
    results = analyze_athletes()
    
    # Exemple de profil d'athlète
    print("\n" + "="*60)
    print("  EXEMPLE: PROFIL D'ATHLETE")
    print("="*60)
    
    # Rechercher un athlète célèbre
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT athlete_full_name
        FROM medals
        WHERE athlete_full_name IS NOT NULL
        GROUP BY athlete_full_name
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    top_athlete_name = cursor.fetchone()['athlete_full_name']
    conn.close()
    
    get_athlete_profile(top_athlete_name)
