"""
Flask API for Olympic Medal Predictions - MySQL AlwaysData Version
Serves ML model predictions trained on REAL historical data
Uses 124 countries and 100,875+ medals from AlwaysData MySQL
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import json

# Add directories to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))

from olympic_predictor_mysql import OlympicPredictorMySQL

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize predictor with MySQL data
predictor = OlympicPredictorMySQL()

# Try to load existing models, otherwise train new ones
try:
    predictor.load_models('./models_mysql')
    print("✅ Models loaded successfully from MySQL training")
except:
    print("⚠️  No existing MySQL models found. Training new models...")
    print("📊 This will use REAL data from AlwaysData MySQL...")
    predictor.train_models()
    predictor.save_models('./models_mysql')
    print("✅ Training complete with real historical data")


@app.route('/api/ml/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Olympic ML Prediction API - MySQL Version',
        'version': '2.0.0',
        'data_source': 'AlwaysData MySQL - Real Historical Data',
        'countries': 124,
        'medals': '100,875+',
        'models': ['Linear Regression (R²=0.801)', 'Random Forest (R²=0.681)']
    })


@app.route('/api/ml/predict/paris2024', methods=['GET'])
def predict_paris_2024():
    """Get predictions for all top countries for Paris 2024"""
    try:
        # Charger les prédictions depuis le fichier JSON
        json_path = os.path.join(os.path.dirname(__file__), 'predictions_paris_2024_mysql.json')
        
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                predictions = json.load(f)
        else:
            # Si pas de fichier, générer les prédictions
            print("📊 Generating predictions from MySQL models...")
            predictions = predictor.predict_top_countries(25)
            
            # Sauvegarder pour la prochaine fois
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(predictions, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'data': predictions,
            'olympics': 'Paris 2024',
            'total_countries': len(predictions),
            'data_source': 'MySQL AlwaysData - 100,875+ historical medals',
            'model_info': {
                'linear_regression': 'R² = 0.801',
                'random_forest': 'R² = 0.681',
                'ensemble': 'Average of both models'
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ml/predict/country/<country_code>', methods=['GET'])
def predict_country(country_code):
    """Get prediction for a specific country by country code"""
    try:
        # Convertir en majuscules
        country_code = country_code.upper()
        
        print(f"📊 Predicting for country: {country_code}")
        prediction = predictor.predict_paris_2024(country_code)
        
        if not prediction:
            return jsonify({
                'success': False,
                'error': f'Country code {country_code} not found in MySQL database'
            }), 404
        
        return jsonify({
            'success': True,
            'data': prediction,
            'olympics': 'Paris 2024',
            'data_source': 'MySQL AlwaysData'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ml/models/info', methods=['GET'])
def get_models_info():
    """Get information about the trained models"""
    return jsonify({
        'success': True,
        'models': {
            'linear_regression': {
                'type': 'Linear Regression',
                'r2_score': 0.801,
                'mae': 12.10,
                'rmse': 26.06,
                'description': 'Linear model trained on historical Olympic data'
            },
            'random_forest': {
                'type': 'Random Forest Regressor',
                'n_estimators': 200,
                'max_depth': 15,
                'r2_score': 0.681,
                'mae': 12.62,
                'rmse': 35.20,
                'description': 'Ensemble model with 200 decision trees'
            }
        },
        'features': {
            'most_important': [
                {'name': 'recent_trend_factor', 'importance': 0.288},
                {'name': 'total_medals', 'importance': 0.223},
                {'name': 'avg_gold_per_olympics', 'importance': 0.198},
                {'name': 'avg_silver_per_olympics', 'importance': 0.165},
                {'name': 'avg_bronze_per_olympics', 'importance': 0.081}
            ]
        },
        'training_data': {
            'countries': 124,
            'total_medals': '100,875+',
            'olympic_games': '1896-2022',
            'source': 'MySQL AlwaysData'
        }
    })


@app.route('/api/ml/retrain', methods=['POST'])
def retrain_models():
    """Retrain models with latest data from MySQL"""
    try:
        print("🔄 Retraining models with latest MySQL data...")
        
        metrics = predictor.train_models()
        predictor.save_models('./models_mysql')
        
        # Regénérer les prédictions
        predictions = predictor.predict_top_countries(25)
        json_path = os.path.join(os.path.dirname(__file__), 'predictions_paris_2024_mysql.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(predictions, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'message': 'Models retrained successfully with MySQL data',
            'metrics': metrics,
            'predictions_generated': len(predictions)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ml/top/<int:limit>', methods=['GET'])
def get_top_predictions(limit):
    """Get top N country predictions"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'predictions_paris_2024_mysql.json')
        
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                predictions = json.load(f)
        else:
            predictions = predictor.predict_top_countries(limit)
        
        # Limiter aux N premiers
        top_predictions = predictions[:limit]
        
        return jsonify({
            'success': True,
            'data': top_predictions,
            'count': len(top_predictions),
            'data_source': 'MySQL AlwaysData'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("  🤖 Olympic ML Prediction API - MySQL Version")
    print("=" * 60)
    print(f"  Data Source: AlwaysData MySQL")
    print(f"  Countries: 124")
    print(f"  Historical Medals: 100,875+")
    print(f"  Olympic Games: 1896-2022")
    print("=" * 60)
    print("\n📊 API Endpoints:")
    print("  - GET  /api/ml/health")
    print("  - GET  /api/ml/predict/paris2024")
    print("  - GET  /api/ml/predict/country/<code>")
    print("  - GET  /api/ml/models/info")
    print("  - GET  /api/ml/top/<limit>")
    print("  - POST /api/ml/retrain")
    print("=" * 60)
    print(f"\n🚀 Server running on http://localhost:5001")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
