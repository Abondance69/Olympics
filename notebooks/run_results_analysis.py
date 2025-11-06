"""
Script pour exécuter l'analyse du notebook results.ipynb
"""
import sys
import os

# Ajouter le répertoire parent au chemin Python
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif
import matplotlib.pyplot as plt
import seaborn as sns
from database.connexion import get_connection

# Configuration
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*70)
print("  🏃 ANALYSE DES RÉSULTATS ET PERFORMANCES DES ATHLÈTES")
print("="*70)

# ============================================================
# 🔌 CONNEXION À LA BASE DE DONNÉES
# ============================================================
print("\n[1/4] Connexion à la base de données...")
conn = get_connection()

# Vérifier les tables disponibles
cursor = conn.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print("\n📋 Tables disponibles :")
for table in tables:
    print(f"   - {table[0]}")

# Essayer de charger la table athletes
try:
    athletes_df = pd.read_sql("SELECT * FROM athletes LIMIT 1000", conn)
    print(f"\n✅ Table 'athletes' chargée : {len(athletes_df)} enregistrements")
    has_athletes = True
except Exception as e:
    print(f"\n⚠️ Erreur chargement 'athletes': {e}")
    has_athletes = False
    athletes_df = None

# Essayer de charger la table results
try:
    results_df = pd.read_sql("SELECT * FROM results LIMIT 1000", conn)
    print(f"✅ Table 'results' chargée : {len(results_df)} enregistrements")
    has_results = True
except Exception as e:
    print(f"⚠️ Erreur chargement 'results': {e}")
    has_results = False
    results_df = None

conn.close()

# Choisir la table à analyser
if has_results and results_df is not None and len(results_df) > 0:
    data_df = results_df
    data_source = "results"
    print(f"\n📊 Analyse de la table 'results' ({len(data_df)} enregistrements)")
elif has_athletes and athletes_df is not None:
    data_df = athletes_df
    data_source = "athletes"
    print(f"\n📊 Analyse de la table 'athletes' ({len(data_df)} enregistrements)")
else:
    print("\n❌ Aucune donnée disponible pour l'analyse")
    data_df = None
    data_source = None

# ============================================================
# 📊 AFFICHER UN APERÇU
# ============================================================
if data_df is not None:
    print("\n[2/4] Aperçu des données...")
    print("\n" + "="*70)
    print(f"📋 Colonnes disponibles ({data_source}):")
    print(data_df.columns.tolist())
    print("\n" + "="*70)
    print(f"📋 Premiers enregistrements:")
    print(data_df.head(3))
    print("\n" + "="*70)
    print("📊 Informations sur les données:")
    print(data_df.info())

# ============================================================
# 📊 STATISTIQUES DESCRIPTIVES
# ============================================================
print("\n[3/4] Calcul des statistiques...")
if data_source == "athletes" and data_df is not None:
    print("\n" + "="*70)
    print("📈 STATISTIQUES GÉNÉRALES SUR LES ATHLÈTES")
    print("="*70)
    
    print(f"\n👥 Nombre total d'athlètes : {len(data_df):,}")
    
    # Analyse par genre
    if "gender" in data_df.columns:
        print("\n⚖️ Répartition par genre :")
        print(data_df["gender"].value_counts())
    
    # Analyse des médailles
    if "total_medals" in data_df.columns:
        total_medals = data_df["total_medals"].sum()
        athletes_with_medals = len(data_df[data_df["total_medals"] > 0])
        print(f"\n🏅 Total de médailles : {total_medals:,}")
        print(f"🏆 Athlètes médaillés : {athletes_with_medals:,}")
        print(f"📊 Moyenne de médailles : {data_df['total_medals'].mean():.2f}")
        
        # Top 10 athlètes
        print("\n🥇 Top 10 des athlètes les plus médaillés :")
        cols_to_show = ["full_name", "total_medals"]
        if "country_id" in data_df.columns:
            cols_to_show.insert(1, "country_id")
        if "gold_medals" in data_df.columns:
            cols_to_show.append("gold_medals")
        if "silver_medals" in data_df.columns:
            cols_to_show.append("silver_medals")
        if "bronze_medals" in data_df.columns:
            cols_to_show.append("bronze_medals")
        
        top_athletes = data_df.nlargest(10, "total_medals")[cols_to_show]
        print(top_athletes.to_string(index=False))
    
    # Analyse physique
    if "height_cm" in data_df.columns and "weight_kg" in data_df.columns:
        print("\n📏 Statistiques physiques :")
        print(f"   Taille moyenne : {data_df['height_cm'].mean():.1f} cm")
        print(f"   Poids moyen : {data_df['weight_kg'].mean():.1f} kg")

elif data_source == "results" and data_df is not None:
    print("\n" + "="*70)
    print("📈 STATISTIQUES SUR LES RÉSULTATS")
    print("="*70)
    
    print(f"\n📊 Nombre total de résultats : {len(data_df):,}")
    
    if "rank_position" in data_df.columns:
        print("\n🏆 Statistiques des classements :")
        print(f"   Meilleure position : {data_df['rank_position'].min()}")
        print(f"   Position moyenne : {data_df['rank_position'].mean():.2f}")
        print(f"   Nombre de podiums (top 3) : {len(data_df[data_df['rank_position'] <= 3]):,}")
    
    if "is_record" in data_df.columns:
        records_count = data_df["is_record"].sum()
        print(f"\n🎯 Nombre de records : {records_count}")

# ============================================================
# 🎯 RÉSUMÉ FINAL
# ============================================================
print("\n[4/4] Génération du résumé...")
if data_df is not None:
    print("\n" + "=" * 70)
    print(f"           📊 RÉSUMÉ DE L'ANALYSE ({data_source.upper()}) 📊")
    print("=" * 70)
    
    if data_source == "athletes":
        print(f"\n👥 Total d'athlètes : {len(data_df):,}")
        
        if "gender" in data_df.columns:
            print(f"\n⚖️ Répartition par genre :")
            for gender, count in data_df["gender"].value_counts().items():
                print(f"   - {gender}: {count:,} athlètes")
        
        if "total_medals" in data_df.columns:
            print(f"\n🏅 Statistiques de médailles :")
            print(f"   - Total : {data_df['total_medals'].sum():,}")
            print(f"   - Athlètes médaillés : {len(data_df[data_df['total_medals'] > 0]):,}")
            print(f"   - Moyenne par athlète : {data_df['total_medals'].mean():.2f}")
            
            # Top 3
            print(f"\n🥇 Top 3 des athlètes :")
            top_3 = data_df.nlargest(3, "total_medals")
            for i, row in enumerate(top_3.itertuples(), 1):
                name = row.full_name if hasattr(row, 'full_name') else 'N/A'
                medals = row.total_medals if hasattr(row, 'total_medals') else 0
                print(f"   {i}. {name} : {medals} médailles")
        
        if "height_cm" in data_df.columns and "weight_kg" in data_df.columns:
            print(f"\n📏 Caractéristiques physiques moyennes :")
            print(f"   - Taille : {data_df['height_cm'].mean():.1f} cm")
            print(f"   - Poids : {data_df['weight_kg'].mean():.1f} kg")
    
    elif data_source == "results":
        print(f"\n📊 Total de résultats : {len(data_df):,}")
        
        if "rank_position" in data_df.columns:
            print(f"\n🏆 Statistiques de classement :")
            print(f"   - Podiums (top 3) : {len(data_df[data_df['rank_position'] <= 3]):,}")
            print(f"   - Position moyenne : {data_df['rank_position'].mean():.2f}")
        
        if "is_record" in data_df.columns:
            records = data_df["is_record"].sum()
            print(f"\n🎯 Records établis : {records}")
    
    print("\n" + "=" * 70)
    print("✅ Analyse terminée avec succès !")
    print("=" * 70)
else:
    print("\n⚠️ Aucune donnée disponible pour générer un résumé.")

print("\n💡 Note: Les visualisations graphiques sont disponibles dans le notebook Jupyter.")
print("   Pour les voir, ouvrez results.ipynb dans VS Code et exécutez les cellules.\n")
