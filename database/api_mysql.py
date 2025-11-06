"""
API Flask pour exposer les données MySQL AlwaysData
Permet au frontend d'accéder aux vraies données via Python
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)  # Permettre les requêtes depuis le frontend

def get_db_connection():
    """Connexion à MySQL AlwaysData"""
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD").strip('"'),
        database=os.getenv("DB_DATABASE"),
        port=int(os.getenv("DB_PORT", 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérifier que l'API fonctionne"""
    return jsonify({"status": "healthy", "message": "MySQL Data API operational"})

@app.route('/api/stats/overview', methods=['GET'])
def get_overview_stats():
    """Statistiques globales RÉELLES"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Nombre total de médailles
        cursor.execute("SELECT COUNT(*) as total FROM medals")
        total_medals = cursor.fetchone()['total']
        
        # Nombre de pays
        cursor.execute("SELECT COUNT(DISTINCT country_name) as total FROM medals")
        total_countries = cursor.fetchone()['total']
        
        # Nombre de Jeux Olympiques
        cursor.execute("SELECT COUNT(*) as total FROM hosts")
        total_hosts = cursor.fetchone()['total']
        
        # Nombre de sports différents
        cursor.execute("SELECT COUNT(DISTINCT discipline_title) as total FROM medals")
        total_sports = cursor.fetchone()['total']
        
        conn.close()
        
        return jsonify({
            "totalMedals": total_medals,
            "totalCountries": total_countries,
            "totalEvents": total_hosts,
            "totalSports": total_sports
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats/france', methods=['GET'])
def get_france_stats():
    """Statistiques de la France RÉELLES"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Médailles de la France
        cursor.execute("""
            SELECT 
                COUNT(*) as total_medals,
                SUM(CASE WHEN medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold,
                SUM(CASE WHEN medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver,
                SUM(CASE WHEN medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze
            FROM medals
            WHERE country_code = 'FR'
        """)
        france_data = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            "totalMedals": france_data['total_medals'],
            "gold": france_data['gold'],
            "silver": france_data['silver'],
            "bronze": france_data['bronze']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/medals/top-countries', methods=['GET'])
def get_top_countries():
    """Top 10 pays avec le plus de médailles"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                country_name,
                country_code,
                COUNT(*) as total_medals,
                SUM(CASE WHEN medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold,
                SUM(CASE WHEN medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver,
                SUM(CASE WHEN medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze
            FROM medals
            GROUP BY country_name, country_code
            ORDER BY total_medals DESC
            LIMIT %s
        """, (limit,))
        
        countries = cursor.fetchall()
        conn.close()
        
        return jsonify(countries)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/medals/by-year', methods=['GET'])
def get_medals_by_year():
    """Distribution des médailles par année"""
    try:
        country = request.args.get('country')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if country:
            cursor.execute("""
                SELECT 
                    h.game_year as year,
                    COUNT(*) as total_medals,
                    SUM(CASE WHEN m.medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold,
                    SUM(CASE WHEN m.medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver,
                    SUM(CASE WHEN m.medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze
                FROM medals m
                JOIN hosts h ON m.slug_game = h.game_slug
                WHERE m.country_code = %s
                GROUP BY h.game_year
                ORDER BY h.game_year
            """, (country,))
        else:
            cursor.execute("""
                SELECT 
                    h.game_year as year,
                    COUNT(*) as total_medals
                FROM medals m
                JOIN hosts h ON m.slug_game = h.game_slug
                GROUP BY h.game_year
                ORDER BY h.game_year
            """)
        
        data = cursor.fetchall()
        conn.close()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/hosts', methods=['GET'])
def get_all_hosts():
    """Liste de tous les Jeux Olympiques"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                game_name,
                game_year,
                game_season,
                game_location,
                game_start_date,
                game_end_date
            FROM hosts
            ORDER BY game_year DESC
        """)
        
        hosts = cursor.fetchall()
        conn.close()
        
        return jsonify(hosts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sports/top', methods=['GET'])
def get_top_sports():
    """Sports avec le plus de médailles"""
    try:
        limit = request.args.get('limit', 10, type=int)
        country = request.args.get('country')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if country:
            cursor.execute("""
                SELECT 
                    discipline_title as sport,
                    COUNT(*) as medals
                FROM medals
                WHERE country_code = %s
                GROUP BY discipline_title
                ORDER BY medals DESC
                LIMIT %s
            """, (country, limit))
        else:
            cursor.execute("""
                SELECT 
                    discipline_title as sport,
                    COUNT(*) as medals
                FROM medals
                GROUP BY discipline_title
                ORDER BY medals DESC
                LIMIT %s
            """, (limit,))
        
        sports = cursor.fetchall()
        conn.close()
        
        return jsonify(sports)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/athletes', methods=['GET'])
def get_athletes():
    """Liste des athlètes avec leurs médailles"""
    try:
        limit = request.args.get('limit', 50, type=int)
        country = request.args.get('country')
        sport = request.args.get('sport')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                athlete_full_name,
                athlete_url,
                country_name,
                country_code,
                COUNT(*) as total_medals,
                SUM(CASE WHEN medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold,
                SUM(CASE WHEN medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver,
                SUM(CASE WHEN medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze
            FROM medals
            WHERE athlete_full_name IS NOT NULL
        """
        
        params = []
        if country:
            query += " AND country_code = %s"
            params.append(country)
        if sport:
            query += " AND discipline_title = %s"
            params.append(sport)
        
        query += """
            GROUP BY athlete_full_name, athlete_url, country_name, country_code
            ORDER BY total_medals DESC
            LIMIT %s
        """
        params.append(limit)
        
        cursor.execute(query, tuple(params))
        athletes = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': athletes,
            'count': len(athletes)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/athletes/top', methods=['GET'])
def get_top_athletes():
    """Top athlètes par nombre de médailles"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                athlete_full_name,
                country_name,
                country_code,
                COUNT(*) as total_medals,
                SUM(CASE WHEN medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold,
                SUM(CASE WHEN medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver,
                SUM(CASE WHEN medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze
            FROM medals
            WHERE athlete_full_name IS NOT NULL
            GROUP BY athlete_full_name, country_name, country_code
            ORDER BY total_medals DESC, gold DESC
            LIMIT %s
        """, (limit,))
        
        athletes = cursor.fetchall()
        conn.close()
        
        return jsonify(athletes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/athletes/by-sport', methods=['GET'])
def get_athletes_by_sport():
    """Athlètes groupés par sport"""
    try:
        limit = request.args.get('limit', 5, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Top sports
        cursor.execute("""
            SELECT DISTINCT discipline_title
            FROM medals
            WHERE discipline_title IS NOT NULL
            ORDER BY discipline_title
        """)
        sports = [row['discipline_title'] for row in cursor.fetchall()]
        
        result = {}
        for sport in sports[:20]:  # Limiter aux 20 premiers sports
            cursor.execute("""
                SELECT 
                    athlete_full_name,
                    country_name,
                    COUNT(*) as medals
                FROM medals
                WHERE discipline_title = %s
                AND athlete_full_name IS NOT NULL
                GROUP BY athlete_full_name, country_name
                ORDER BY medals DESC
                LIMIT %s
            """, (sport, limit))
            
            result[sport] = cursor.fetchall()
        
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/athletes/legends', methods=['GET'])
def get_athlete_legends():
    """Légendes olympiques (athlètes avec 5+ médailles d'or)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                athlete_full_name,
                country_name,
                country_code,
                COUNT(*) as total_medals,
                SUM(CASE WHEN medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold,
                SUM(CASE WHEN medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver,
                SUM(CASE WHEN medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze,
                GROUP_CONCAT(DISTINCT discipline_title) as sports
            FROM medals
            WHERE athlete_full_name IS NOT NULL
            GROUP BY athlete_full_name, country_name, country_code
            HAVING gold >= 5
            ORDER BY gold DESC, total_medals DESC
            LIMIT 50
        """)
        
        legends = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': legends,
            'count': len(legends),
            'criteria': 'Athletes with 5+ gold medals'
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/athletes/stats', methods=['GET'])
def get_athletes_stats():
    """Statistiques générales sur les athlètes"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Nombre total d'athlètes uniques
        cursor.execute("""
            SELECT COUNT(DISTINCT athlete_full_name) as total
            FROM medals
            WHERE athlete_full_name IS NOT NULL
        """)
        total_athletes = cursor.fetchone()['total']
        
        # Athlète avec le plus de médailles
        cursor.execute("""
            SELECT 
                athlete_full_name,
                country_name,
                COUNT(*) as medals
            FROM medals
            WHERE athlete_full_name IS NOT NULL
            GROUP BY athlete_full_name, country_name
            ORDER BY medals DESC
            LIMIT 1
        """)
        top_athlete = cursor.fetchone()
        
        # Athlète avec le plus de médailles d'or
        cursor.execute("""
            SELECT 
                athlete_full_name,
                country_name,
                SUM(CASE WHEN medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold
            FROM medals
            WHERE athlete_full_name IS NOT NULL
            GROUP BY athlete_full_name, country_name
            ORDER BY gold DESC
            LIMIT 1
        """)
        top_gold_athlete = cursor.fetchone()
        
        # Pays avec le plus d'athlètes médaillés
        cursor.execute("""
            SELECT 
                country_name,
                COUNT(DISTINCT athlete_full_name) as athletes
            FROM medals
            WHERE athlete_full_name IS NOT NULL
            GROUP BY country_name
            ORDER BY athletes DESC
            LIMIT 5
        """)
        top_countries_athletes = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            'total_athletes': total_athletes,
            'top_medalist': top_athlete,
            'top_gold_medalist': top_gold_athlete,
            'countries_with_most_athletes': top_countries_athletes
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("  API MySQL AlwaysData - Demarrage")
    print("=" * 60)
    print(f"  Host MySQL: {os.getenv('DB_HOST')}")
    print(f"  Database: {os.getenv('DB_DATABASE')}")
    print(f"  API Port: 5002")
    print("=" * 60)
    print("\nEndpoints disponibles:")
    print("  - GET  /api/health")
    print("  - GET  /api/stats/overview")
    print("  - GET  /api/stats/france")
    print("  - GET  /api/medals/top-countries?limit=10")
    print("  - GET  /api/medals/by-year?country=FR")
    print("  - GET  /api/hosts")
    print("  - GET  /api/sports/top?limit=10&country=FR")
    print("  - GET  /api/athletes?limit=50&country=FR&sport=Athletics")
    print("  - GET  /api/athletes/top?limit=10")
    print("  - GET  /api/athletes/by-sport?limit=5")
    print("  - GET  /api/athletes/legends")
    print("  - GET  /api/athletes/stats")
    print("=" * 60)
    print("\nServer running on http://localhost:5002")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5002, debug=True)
