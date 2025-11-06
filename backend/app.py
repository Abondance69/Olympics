"""
🏅 Olympics Analytics - Backend API Principal (Python/Flask)
API consolidée qui regroupe toutes les routes nécessaires
Basée sur les données MySQL AlwaysData + Prédictions ML
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
from dotenv import load_dotenv
import os
import sys

# Charger les variables d'environnement
load_dotenv()

# Ajouter le dossier parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml-models'))

# Initialiser Flask
app = Flask(__name__)
CORS(app)  # Permettre les requêtes depuis le frontend

# ============================================
# CONNEXION BASE DE DONNÉES
# ============================================

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

# ============================================
# A. API GÉNÉRALES (INFOS DE BASE)
# ============================================

@app.route('/', methods=['GET'])
@app.route('/api', methods=['GET'])
def api_root():
    """Message d'accueil ou statut API"""
    return jsonify({
        'message': 'Olympics Analytics API - Backend Principal',
        'version': '1.0.0',
        'status': 'operational',
        'data_source': 'MySQL AlwaysData + ML Models',
        'endpoints': {
            'health': '/api/health',
            'stats': {
                'overview': '/api/stats/overview',
                'france': '/api/stats/france',
                'medals_by_country': '/api/stats/medals-by-country',
                'medals_by_year': '/api/stats/medals-by-year',
                'medals_by_discipline': '/api/stats/medals-by-discipline',
                'gender_ratio': '/api/stats/gender-ratio',
                'age_distribution': '/api/stats/age-distribution',
                'hosts_summary': '/api/stats/hosts-summary'
            },
            'hosts': '/api/hosts',
            'countries': '/api/countries',
            'athletes': '/api/athletes',
            'results': '/api/results',
            'predictions': '/api/predictions/paris2024'
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérifier que l'API fonctionne"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'message': 'API operational',
            'database': 'connected',
            'timestamp': os.popen('echo %date% %time%').read().strip()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# ============================================
# /HOSTS - Liste de tous les Jeux Olympiques
# ============================================

@app.route('/api/hosts', methods=['GET'])
def get_all_hosts():
    """
    Liste de tous les Jeux Olympiques (année, ville, saison...)
    Utilisation: Dropdown ou timeline sur le site
    """
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
        
        return jsonify({
            'success': True,
            'data': hosts,
            'count': len(hosts)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/hosts/<int:year>', methods=['GET'])
def get_host_by_year(year):
    """
    Détails des JO d'une année donnée
    Utilisation: Page de détails d'un événement
    """
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
            WHERE game_year = %s
        """, (year,))
        
        hosts = cursor.fetchall()
        conn.close()
        
        if not hosts:
            return jsonify({
                'success': False,
                'error': f'No Olympics found for year {year}'
            }), 404
        
        return jsonify({
            'success': True,
            'data': hosts
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# /ATHLETES - Liste paginée d'athlètes
# ============================================

@app.route('/api/athletes', methods=['GET'])
def get_athletes():
    """
    Liste paginée d'athlètes
    Utilisation: Liste d'athlètes avec recherche
    Query params: limit, country, sport
    """
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
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/athletes/<path:name>', methods=['GET'])
def get_athlete_by_name(name):
    """
    Fiche détaillée d'un athlète
    Utilisation: Profil d'un athlète
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                athlete_full_name,
                athlete_url,
                country_name,
                country_code,
                COUNT(*) as total_medals,
                SUM(CASE WHEN medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold,
                SUM(CASE WHEN medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver,
                SUM(CASE WHEN medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze,
                GROUP_CONCAT(DISTINCT discipline_title) as sports
            FROM medals
            WHERE athlete_full_name = %s
            GROUP BY athlete_full_name, athlete_url, country_name, country_code
        """, (name,))
        
        athlete = cursor.fetchone()
        conn.close()
        
        if not athlete:
            return jsonify({
                'success': False,
                'error': f'Athlete {name} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': athlete
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# /RESULTS - Tous les résultats filtrables
# ============================================

@app.route('/api/results', methods=['GET'])
def get_results():
    """
    Tous les résultats (discipline, médaille, pays, etc.)
    Utilisation: Table des résultats filtrables
    Query params: country, sport, year, medal_type, limit
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        country = request.args.get('country')
        sport = request.args.get('sport')
        year = request.args.get('year', type=int)
        medal_type = request.args.get('medal_type')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                m.athlete_full_name,
                m.country_name,
                m.country_code,
                m.discipline_title,
                m.event_title,
                m.medal_type,
                h.game_year,
                h.game_location,
                h.game_season
            FROM medals m
            JOIN hosts h ON m.slug_game = h.game_slug
            WHERE 1=1
        """
        
        params = []
        if country:
            query += " AND m.country_code = %s"
            params.append(country)
        if sport:
            query += " AND m.discipline_title = %s"
            params.append(sport)
        if year:
            query += " AND h.game_year = %s"
            params.append(year)
        if medal_type:
            query += " AND m.medal_type = %s"
            params.append(medal_type.upper())
        
        query += " ORDER BY h.game_year DESC, m.medal_type LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results),
            'filters': {
                'country': country,
                'sport': sport,
                'year': year,
                'medal_type': medal_type,
                'limit': limit
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# /COUNTRIES - Liste des pays participants
# ============================================

@app.route('/api/countries', methods=['GET'])
def get_countries():
    """
    Liste des pays participants
    Utilisation: Dropdown de filtres par pays
    """
    try:
        limit = request.args.get('limit', 200, type=int)
        
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
        
        return jsonify({
            'success': True,
            'data': countries,
            'count': len(countries)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# B. API ANALYTIQUES (STATS DYNAMIQUES)
# ============================================

@app.route('/api/stats/overview', methods=['GET'])
def get_overview_stats():
    """Statistiques globales pour le dashboard principal"""
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
        
        # Nombre d'athlètes uniques (basé sur le nom complet)
        cursor.execute("SELECT COUNT(DISTINCT athlete_full_name) as total FROM medals WHERE athlete_full_name IS NOT NULL")
        total_athletes = cursor.fetchone()['total']
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'totalMedals': total_medals,
                'totalCountries': total_countries,
                'totalEvents': total_hosts,
                'totalAthletes': total_athletes
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats/france', methods=['GET'])
def get_france_stats():
    """Statistiques spécifiques à la France"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
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
            'success': True,
            'data': france_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats/medals-by-country', methods=['GET'])
def get_medals_by_country():
    """
    Retourne le total de médailles par pays
    Utilisation: Graphique "Top 10 pays"
    """
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
        
        return jsonify({
            'success': True,
            'data': countries
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats/medals-by-year', methods=['GET'])
def get_medals_by_year():
    """
    Retourne la répartition des médailles par année
    Utilisation: Graphique d'évolution
    """
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
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats/medals-by-discipline', methods=['GET'])
def get_medals_by_discipline():
    """
    Retourne le nombre de médailles par discipline
    Utilisation: Diagramme circulaire ou barres
    """
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
        
        return jsonify({
            'success': True,
            'data': sports
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats/gender-ratio', methods=['GET'])
def get_gender_ratio():
    """
    Ratio hommes/femmes parmi les athlètes
    Utilisation: Donut chart
    """
    # Pour l'instant, retourner des données estimées
    # TODO: Ajouter les données de genre à la base de données
    return jsonify({
        'success': True,
        'data': {
            'male': 55,
            'female': 45
        },
        'note': 'Estimated based on historical Olympic data'
    })

@app.route('/api/stats/age-distribution', methods=['GET'])
def get_age_distribution():
    """
    Distribution des âges des athlètes
    Utilisation: Histogramme dynamique
    """
    # Pour l'instant, retourner des données estimées
    # TODO: Ajouter les données d'âge à la base de données
    age_groups = [
        {'range': '15-20', 'count': 1250},
        {'range': '21-25', 'count': 3500},
        {'range': '26-30', 'count': 4200},
        {'range': '31-35', 'count': 2100},
        {'range': '36-40', 'count': 850},
        {'range': '41+', 'count': 320}
    ]
    
    return jsonify({
        'success': True,
        'data': age_groups,
        'note': 'Estimated distribution'
    })

@app.route('/api/stats/hosts-summary', methods=['GET'])
def get_hosts_summary():
    """
    Nombre de JO par continent ou saison
    Utilisation: Dashboard principal
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM hosts ORDER BY game_year DESC")
        hosts = cursor.fetchall()
        
        summary = {
            'total': len(hosts),
            'by_season': {
                'summer': len([h for h in hosts if h['game_season'] == 'Summer']),
                'winter': len([h for h in hosts if h['game_season'] == 'Winter'])
            },
            'most_recent': hosts[:5] if len(hosts) >= 5 else hosts
        }
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# C. API IA / PRÉDICTION
# ============================================

@app.route('/api/predictions/paris2024', methods=['GET'])
def get_predictions_paris2024():
    """
    Prédictions pour Paris 2024
    Charge les prédictions depuis le fichier JSON généré par le modèle ML
    """
    try:
        import json
        
        # Charger les prédictions depuis le fichier
        predictions_file = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'ml-models', 
            'predictions_paris_2024_mysql.json'
        )
        
        if os.path.exists(predictions_file):
            with open(predictions_file, 'r', encoding='utf-8') as f:
                predictions = json.load(f)
            
            return jsonify({
                'success': True,
                'data': predictions,
                'olympics': 'Paris 2024',
                'total_countries': len(predictions),
                'data_source': 'MySQL AlwaysData - ML Predictions'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Predictions file not found. Please train the ML model first.'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predictions/country/<country_code>', methods=['GET'])
def get_prediction_by_country(country_code):
    """
    Prédiction pour un pays spécifique
    """
    try:
        import json
        
        predictions_file = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'ml-models', 
            'predictions_paris_2024_mysql.json'
        )
        
        if os.path.exists(predictions_file):
            with open(predictions_file, 'r', encoding='utf-8') as f:
                predictions = json.load(f)
            
            # Chercher le pays
            country_prediction = next(
                (p for p in predictions if p['country_code'] == country_code.upper()), 
                None
            )
            
            if country_prediction:
                return jsonify({
                    'success': True,
                    'data': country_prediction,
                    'olympics': 'Paris 2024'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'No prediction found for country {country_code}'
                }), 404
        else:
            return jsonify({
                'success': False,
                'error': 'Predictions file not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# GESTION D'ERREURS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ============================================
# LANCEMENT DU SERVEUR
# ============================================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  🏅 OLYMPICS ANALYTICS - BACKEND API PRINCIPAL")
    print("=" * 60)
    print(f"  Database: {os.getenv('DB_DATABASE')} @ {os.getenv('DB_HOST')}")
    print(f"  Port: 5000")
    print("=" * 60)
    print("\n📊 Endpoints disponibles:")
    print("\n  A. API Générales (infos de base)")
    print("    GET  /api/health")
    print("    GET  /api/hosts")
    print("    GET  /api/hosts/<year>")
    print("    GET  /api/athletes?limit=50&country=FR&sport=Athletics")
    print("    GET  /api/athletes/<name>")
    print("    GET  /api/results?country=FR&sport=Athletics")
    print("    GET  /api/countries")
    print("\n  B. API Analytiques (stats dynamiques)")
    print("    GET  /api/stats/overview")
    print("    GET  /api/stats/france")
    print("    GET  /api/stats/medals-by-country?limit=10")
    print("    GET  /api/stats/medals-by-year?country=FR")
    print("    GET  /api/stats/medals-by-discipline?limit=10&country=FR")
    print("    GET  /api/stats/gender-ratio")
    print("    GET  /api/stats/age-distribution")
    print("    GET  /api/stats/hosts-summary")
    print("\n  C. API IA / Prédiction")
    print("    GET  /api/predictions/paris2024")
    print("    GET  /api/predictions/country/<code>")
    print("=" * 60)
    print(f"\n🚀 Server running on http://localhost:5000")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
