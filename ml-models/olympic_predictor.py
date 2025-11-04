"""
Olympic Medal Prediction Model
Uses Machine Learning to predict medal counts for Paris 2024 Olympics
Based on historical data from 1896-2022
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json

class OlympicPredictor:
    def __init__(self):
        self.linear_model = None
        self.rf_model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'historical_gold',
            'historical_silver', 
            'historical_bronze',
            'avg_medals_per_olympics',
            'participation_count',
            'recent_performance_trend',
            'gdp_factor',
            'population_factor'
        ]
        
    def create_synthetic_training_data(self):
        """
        Create synthetic training data based on Olympic historical patterns
        In production, this would load from actual historical database
        """
        # Top performing countries with realistic historical data
        countries_data = {
            'USA': {'gold': 1022, 'silver': 795, 'bronze': 705, 'olympics': 28, 'gdp': 1.0, 'pop': 0.9},
            'USSR/Russia': {'gold': 440, 'silver': 357, 'bronze': 325, 'olympics': 20, 'gdp': 0.7, 'pop': 0.6},
            'Germany': {'gold': 283, 'silver': 282, 'bronze': 289, 'olympics': 24, 'gdp': 0.9, 'pop': 0.4},
            'Great Britain': {'gold': 285, 'silver': 316, 'bronze': 315, 'olympics': 28, 'gdp': 0.8, 'pop': 0.3},
            'France': {'gold': 248, 'silver': 276, 'bronze': 316, 'olympics': 28, 'gdp': 0.8, 'pop': 0.3},
            'Italy': {'gold': 217, 'silver': 188, 'bronze': 213, 'olympics': 27, 'gdp': 0.7, 'pop': 0.3},
            'China': {'gold': 262, 'silver': 199, 'bronze': 173, 'olympics': 11, 'gdp': 0.95, 'pop': 1.0},
            'Australia': {'gold': 164, 'silver': 173, 'bronze': 210, 'olympics': 27, 'gdp': 0.6, 'pop': 0.1},
            'Japan': {'gold': 169, 'silver': 150, 'bronze': 178, 'olympics': 23, 'gdp': 0.75, 'pop': 0.5},
            'Netherlands': {'gold': 95, 'silver': 105, 'bronze': 122, 'olympics': 26, 'gdp': 0.6, 'pop': 0.08},
            'Canada': {'gold': 71, 'silver': 109, 'bronze': 148, 'olympics': 26, 'gdp': 0.65, 'pop': 0.2},
            'South Korea': {'gold': 96, 'silver': 91, 'bronze': 100, 'olympics': 17, 'gdp': 0.7, 'pop': 0.25},
            'Brazil': {'gold': 37, 'silver': 42, 'bronze': 71, 'olympics': 22, 'gdp': 0.6, 'pop': 0.8},
            'Spain': {'gold': 47, 'silver': 73, 'bronze': 47, 'olympics': 23, 'gdp': 0.65, 'pop': 0.22},
            'Kenya': {'gold': 35, 'silver': 42, 'bronze': 36, 'olympics': 14, 'gdp': 0.2, 'pop': 0.25},
        }
        
        X = []
        y = []
        country_names = []
        
        for country, data in countries_data.items():
            # Calculate features
            avg_medals = (data['gold'] + data['silver'] + data['bronze']) / data['olympics']
            trend = 1.05 if country in ['China', 'USA', 'Great Britain'] else 0.98
            
            features = [
                data['gold'] / data['olympics'],  # avg gold per olympics
                data['silver'] / data['olympics'],  # avg silver
                data['bronze'] / data['olympics'],  # avg bronze
                avg_medals,
                data['olympics'],
                trend,
                data['gdp'],
                data['pop']
            ]
            
            # Target: predicted medals for next olympics (with some variance)
            next_gold = data['gold'] / data['olympics'] * trend * (1 + np.random.uniform(-0.1, 0.1))
            next_silver = data['silver'] / data['olympics'] * trend * (1 + np.random.uniform(-0.1, 0.1))
            next_bronze = data['bronze'] / data['olympics'] * trend * (1 + np.random.uniform(-0.1, 0.1))
            
            X.append(features)
            y.append([next_gold, next_silver, next_bronze])
            country_names.append(country)
        
        return np.array(X), np.array(y), country_names
    
    def train_models(self):
        """Train both Linear Regression and Random Forest models"""
        print("🤖 Training Machine Learning Models...")
        
        # Get training data
        X, y, countries = self.create_synthetic_training_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Linear Regression
        print("Training Linear Regression...")
        self.linear_model = LinearRegression()
        self.linear_model.fit(X_train_scaled, y_train)
        
        # Train Random Forest
        print("Training Random Forest...")
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.rf_model.fit(X_train_scaled, y_train)
        
        # Evaluate models
        print("\n📊 Model Evaluation:")
        for name, model in [('Linear Regression', self.linear_model), 
                            ('Random Forest', self.rf_model)]:
            y_pred = model.predict(X_test_scaled)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            print(f"\n{name}:")
            print(f"  MAE: {mae:.2f}")
            print(f"  RMSE: {rmse:.2f}")
            print(f"  R² Score: {r2:.3f}")
        
        return True
    
    def predict_paris_2024(self, country_name, historical_data):
        """
        Predict medals for Paris 2024 for a specific country
        
        Args:
            country_name: Name of the country
            historical_data: Dict with keys: gold, silver, bronze, olympics, gdp, pop
        
        Returns:
            Dict with predictions from both models
        """
        # Prepare features
        total_medals = historical_data['gold'] + historical_data['silver'] + historical_data['bronze']
        avg_medals = total_medals / historical_data['olympics']
        
        # Trend estimation (simple heuristic)
        trend = 1.05 if country_name in ['China', 'USA', 'Great Britain', 'France'] else 1.0
        
        features = np.array([[
            historical_data['gold'] / historical_data['olympics'],
            historical_data['silver'] / historical_data['olympics'],
            historical_data['bronze'] / historical_data['olympics'],
            avg_medals,
            historical_data['olympics'],
            trend,
            historical_data.get('gdp', 0.5),
            historical_data.get('pop', 0.5)
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predictions
        lr_pred = self.linear_model.predict(features_scaled)[0]
        rf_pred = self.rf_model.predict(features_scaled)[0]
        
        # Ensemble prediction (average)
        ensemble_pred = (lr_pred + rf_pred) / 2
        
        return {
            'country': country_name,
            'predictions': {
                'linear_regression': {
                    'gold': max(0, int(round(lr_pred[0]))),
                    'silver': max(0, int(round(lr_pred[1]))),
                    'bronze': max(0, int(round(lr_pred[2]))),
                    'total': max(0, int(round(sum(lr_pred))))
                },
                'random_forest': {
                    'gold': max(0, int(round(rf_pred[0]))),
                    'silver': max(0, int(round(rf_pred[1]))),
                    'bronze': max(0, int(round(rf_pred[2]))),
                    'total': max(0, int(round(sum(rf_pred))))
                },
                'ensemble': {
                    'gold': max(0, int(round(ensemble_pred[0]))),
                    'silver': max(0, int(round(ensemble_pred[1]))),
                    'bronze': max(0, int(round(ensemble_pred[2]))),
                    'total': max(0, int(round(sum(ensemble_pred))))
                }
            },
            'confidence': 0.85  # Mock confidence score
        }
    
    def predict_top_countries(self):
        """Generate predictions for top 25 countries for Paris 2024"""
        countries_data = {
            'USA': {'gold': 1022, 'silver': 795, 'bronze': 705, 'olympics': 28, 'gdp': 1.0, 'pop': 0.9},
            'China': {'gold': 262, 'silver': 199, 'bronze': 173, 'olympics': 11, 'gdp': 0.95, 'pop': 1.0},
            'Great Britain': {'gold': 285, 'silver': 316, 'bronze': 315, 'olympics': 28, 'gdp': 0.8, 'pop': 0.3},
            'France': {'gold': 248, 'silver': 276, 'bronze': 316, 'olympics': 28, 'gdp': 0.8, 'pop': 0.3},
            'Russia': {'gold': 440, 'silver': 357, 'bronze': 325, 'olympics': 20, 'gdp': 0.7, 'pop': 0.6},
            'Germany': {'gold': 283, 'silver': 282, 'bronze': 289, 'olympics': 24, 'gdp': 0.9, 'pop': 0.4},
            'Italy': {'gold': 217, 'silver': 188, 'bronze': 213, 'olympics': 27, 'gdp': 0.7, 'pop': 0.3},
            'Australia': {'gold': 164, 'silver': 173, 'bronze': 210, 'olympics': 27, 'gdp': 0.6, 'pop': 0.1},
            'Japan': {'gold': 169, 'silver': 150, 'bronze': 178, 'olympics': 23, 'gdp': 0.75, 'pop': 0.5},
            'Netherlands': {'gold': 95, 'silver': 105, 'bronze': 122, 'olympics': 26, 'gdp': 0.6, 'pop': 0.08},
            'South Korea': {'gold': 96, 'silver': 91, 'bronze': 100, 'olympics': 17, 'gdp': 0.7, 'pop': 0.25},
            'Canada': {'gold': 71, 'silver': 109, 'bronze': 148, 'olympics': 26, 'gdp': 0.65, 'pop': 0.2},
            'Spain': {'gold': 47, 'silver': 73, 'bronze': 47, 'olympics': 23, 'gdp': 0.65, 'pop': 0.22},
            'Brazil': {'gold': 37, 'silver': 42, 'bronze': 71, 'olympics': 22, 'gdp': 0.6, 'pop': 0.8},
            'Kenya': {'gold': 35, 'silver': 42, 'bronze': 36, 'olympics': 14, 'gdp': 0.2, 'pop': 0.25},
            'Jamaica': {'gold': 26, 'silver': 36, 'bronze': 25, 'olympics': 17, 'gdp': 0.15, 'pop': 0.01},
            'New Zealand': {'gold': 51, 'silver': 32, 'bronze': 50, 'olympics': 24, 'gdp': 0.5, 'pop': 0.02},
            'Cuba': {'gold': 78, 'silver': 68, 'bronze': 80, 'olympics': 20, 'gdp': 0.3, 'pop': 0.05},
            'Poland': {'gold': 72, 'silver': 89, 'bronze': 137, 'olympics': 21, 'gdp': 0.55, 'pop': 0.18},
            'Switzerland': {'gold': 56, 'silver': 78, 'bronze': 72, 'olympics': 28, 'gdp': 0.7, 'pop': 0.04},
            'Denmark': {'gold': 48, 'silver': 78, 'bronze': 77, 'olympics': 27, 'gdp': 0.6, 'pop': 0.03},
            'Sweden': {'gold': 148, 'silver': 176, 'bronze': 179, 'olympics': 28, 'gdp': 0.6, 'pop': 0.05},
            'Norway': {'gold': 60, 'silver': 53, 'bronze': 50, 'olympics': 25, 'gdp': 0.55, 'pop': 0.03},
            'Belgium': {'gold': 44, 'silver': 55, 'bronze': 58, 'olympics': 26, 'gdp': 0.55, 'pop': 0.06},
            'India': {'gold': 10, 'silver': 9, 'bronze': 16, 'olympics': 24, 'gdp': 0.8, 'pop': 1.0},
        }
        
        predictions = []
        for country, data in countries_data.items():
            pred = self.predict_paris_2024(country, data)
            predictions.append(pred)
        
        # Sort by total predicted medals (ensemble)
        predictions.sort(
            key=lambda x: x['predictions']['ensemble']['total'], 
            reverse=True
        )
        
        return predictions[:25]
    
    def save_models(self, path='./models'):
        """Save trained models to disk"""
        import os
        os.makedirs(path, exist_ok=True)
        
        joblib.dump(self.linear_model, f'{path}/linear_model.pkl')
        joblib.dump(self.rf_model, f'{path}/random_forest_model.pkl')
        joblib.dump(self.scaler, f'{path}/scaler.pkl')
        print(f"✅ Models saved to {path}/")
    
    def load_models(self, path='./models'):
        """Load trained models from disk"""
        self.linear_model = joblib.load(f'{path}/linear_model.pkl')
        self.rf_model = joblib.load(f'{path}/random_forest_model.pkl')
        self.scaler = joblib.load(f'{path}/scaler.pkl')
        print(f"✅ Models loaded from {path}/")


def main():
    """Main training and prediction pipeline"""
    print("=" * 50)
    print("🏅 OLYMPIC MEDAL PREDICTION SYSTEM")
    print("=" * 50)
    
    # Initialize predictor
    predictor = OlympicPredictor()
    
    # Train models
    predictor.train_models()
    
    # Save models
    predictor.save_models()
    
    # Generate predictions for Paris 2024
    print("\n" + "=" * 50)
    print("🔮 PREDICTIONS FOR PARIS 2024")
    print("=" * 50)
    
    predictions = predictor.predict_top_countries()
    
    # Display top 10
    print("\n🏆 TOP 10 PREDICTED COUNTRIES:\n")
    for i, pred in enumerate(predictions[:10], 1):
        ens = pred['predictions']['ensemble']
        print(f"{i:2}. {pred['country']:15} - Gold: {ens['gold']:2} | Silver: {ens['silver']:2} | Bronze: {ens['bronze']:2} | Total: {ens['total']:3}")
    
    # Save predictions to JSON
    with open('predictions_paris_2024.json', 'w') as f:
        json.dump(predictions, f, indent=2)
    
    print("\n✅ Predictions saved to predictions_paris_2024.json")
    print("=" * 50)


if __name__ == "__main__":
    main()
