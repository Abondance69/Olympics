"""
Flask API for Olympic Medal Predictions
Serves ML model predictions via REST API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add ml-models directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from olympic_predictor import OlympicPredictor

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize predictor
predictor = OlympicPredictor()

# Try to load existing models, otherwise train new ones
try:
    predictor.load_models('./models')
    print("✅ Models loaded successfully")
except:
    print("⚠️  No existing models found. Training new models...")
    predictor.train_models()
    predictor.save_models('./models')


@app.route('/api/ml/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Olympic ML Prediction API',
        'version': '1.0.0'
    })


@app.route('/api/ml/predict/paris2024', methods=['GET'])
def predict_paris_2024():
    """Get predictions for all top countries for Paris 2024"""
    try:
        predictions = predictor.predict_top_countries()
        return jsonify({
            'success': True,
            'data': predictions,
            'olympics': 'Paris 2024',
            'total_countries': len(predictions)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ml/predict/country/<country_name>', methods=['GET'])
def predict_country(country_name):
    """Get prediction for a specific country"""
    # Sample historical data (would come from database in production)
    countries_data = {
        'USA': {'gold': 1022, 'silver': 795, 'bronze': 705, 'olympics': 28, 'gdp': 1.0, 'pop': 0.9},
        'China': {'gold': 262, 'silver': 199, 'bronze': 173, 'olympics': 11, 'gdp': 0.95, 'pop': 1.0},
        'France': {'gold': 248, 'silver': 276, 'bronze': 316, 'olympics': 28, 'gdp': 0.8, 'pop': 0.3},
        'Great Britain': {'gold': 285, 'silver': 316, 'bronze': 315, 'olympics': 28, 'gdp': 0.8, 'pop': 0.3},
        'Germany': {'gold': 283, 'silver': 282, 'bronze': 289, 'olympics': 24, 'gdp': 0.9, 'pop': 0.4},
        'Japan': {'gold': 169, 'silver': 150, 'bronze': 178, 'olympics': 23, 'gdp': 0.75, 'pop': 0.5},
    }
    
    country_name = country_name.title()
    
    if country_name not in countries_data:
        return jsonify({
            'success': False,
            'error': f'Country {country_name} not found in database'
        }), 404
    
    try:
        prediction = predictor.predict_paris_2024(
            country_name, 
            countries_data[country_name]
        )
        return jsonify({
            'success': True,
            'data': prediction
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ml/models/info', methods=['GET'])
def models_info():
    """Get information about the ML models"""
    return jsonify({
        'success': True,
        'models': [
            {
                'name': 'Linear Regression',
                'type': 'Regression',
                'description': 'Simple linear model for baseline predictions',
                'features': predictor.feature_names
            },
            {
                'name': 'Random Forest',
                'type': 'Ensemble',
                'description': 'Advanced ensemble model with 100 decision trees',
                'features': predictor.feature_names
            }
        ],
        'ensemble': 'Average of both models for final prediction'
    })


@app.route('/api/ml/retrain', methods=['POST'])
def retrain_models():
    """Retrain models with new data"""
    try:
        predictor.train_models()
        predictor.save_models('./models')
        return jsonify({
            'success': True,
            'message': 'Models retrained successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🤖 Starting Olympic ML Prediction API")
    print("=" * 60)
    print("📊 API Endpoints:")
    print("  - GET  /api/ml/health")
    print("  - GET  /api/ml/predict/paris2024")
    print("  - GET  /api/ml/predict/country/<name>")
    print("  - GET  /api/ml/models/info")
    print("  - POST /api/ml/retrain")
    print("=" * 60)
    print("\n🚀 Server running on http://localhost:5001")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
