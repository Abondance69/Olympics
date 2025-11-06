"""
Olympic Medal Prediction Model - MySQL AlwaysData Version
Uses REAL historical data from AlwaysData MySQL database
Trains ML models on 21,697 actual Olympic medals
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
import os
import sys

# Ajouter le dossier database au path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
from connexion import get_connection

class OlympicPredictorMySQL:
    def __init__(self):
        self.linear_model = None
        self.rf_model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'avg_gold_per_olympics',
            'avg_silver_per_olympics', 
            'avg_bronze_per_olympics',
            'olympics_participated',
            'total_medals',
            'gold_ratio',
            'recent_trend_factor',
            'medal_diversity_score'
        ]
        
    def load_data_from_mysql(self):
        """
        Load REAL historical data from AlwaysData MySQL
        Returns: DataFrame with country statistics
        """
        print("📊 Chargement des donnees REELLES depuis MySQL AlwaysData...")
        
        conn = get_connection()
        if not conn:
            raise Exception("Impossible de se connecter a la base de donnees")
        
        cursor = conn.cursor()
        
        # Requête pour obtenir les statistiques par pays
        query = """
        SELECT 
            m.country_name,
            m.country_code,
            COUNT(DISTINCT h.game_slug) as olympics_participated,
            COUNT(*) as total_medals,
            SUM(CASE WHEN m.medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold_medals,
            SUM(CASE WHEN m.medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver_medals,
            SUM(CASE WHEN m.medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze_medals,
            MIN(h.game_year) as first_participation,
            MAX(h.game_year) as last_participation
        FROM medals m
        JOIN hosts h ON m.slug_game = h.game_slug
        WHERE m.country_name IS NOT NULL 
        AND m.country_code IS NOT NULL
        GROUP BY m.country_name, m.country_code
        HAVING total_medals >= 10
        ORDER BY total_medals DESC
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Créer DataFrame
        df = pd.DataFrame(rows, columns=[
            'country_name', 'country_code', 'olympics_participated', 
            'total_medals', 'gold_medals', 'silver_medals', 'bronze_medals',
            'first_participation', 'last_participation'
        ])
        
        # Convertir en types numériques Python
        numeric_cols = ['olympics_participated', 'total_medals', 'gold_medals', 
                       'silver_medals', 'bronze_medals', 'first_participation', 'last_participation']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Médailles récentes (derniers 3 JO)
        recent_query = """
        SELECT 
            m.country_code,
            COUNT(*) as recent_medals
        FROM medals m
        JOIN hosts h ON m.slug_game = h.game_slug
        WHERE h.game_year >= 2012
        GROUP BY m.country_code
        """
        cursor.execute(recent_query)
        recent_data = pd.DataFrame(cursor.fetchall(), columns=['country_code', 'recent_medals'])
        
        conn.close()
        
        # Merger les données récentes
        df = df.merge(recent_data, on='country_code', how='left')
        df['recent_medals'] = pd.to_numeric(df['recent_medals'].fillna(0), errors='coerce')
        
        print(f"   ✅ {len(df)} pays charges depuis MySQL")
        print(f"   ✅ {df['total_medals'].sum():,} medailles historiques")
        
        return df
    
    def prepare_features(self, df):
        """
        Prépare les features à partir des données MySQL
        """
        print("🔧 Preparation des features pour le ML...")
        
        # Calculer les features
        df['avg_gold_per_olympics'] = df['gold_medals'] / df['olympics_participated']
        df['avg_silver_per_olympics'] = df['silver_medals'] / df['olympics_participated']
        df['avg_bronze_per_olympics'] = df['bronze_medals'] / df['olympics_participated']
        df['gold_ratio'] = df['gold_medals'] / df['total_medals']
        
        # Tendance récente (ratio médailles récentes vs moyenne historique)
        df['avg_medals_per_olympics'] = df['total_medals'] / df['olympics_participated']
        df['recent_trend_factor'] = df['recent_medals'] / (df['avg_medals_per_olympics'] * 3 + 1)
        
        # Score de diversité (répartition équilibrée des médailles)
        df['medal_diversity_score'] = 1 - np.abs(
            (df['gold_medals'] - df['silver_medals'] - df['bronze_medals']) / df['total_medals']
        )
        
        # Features pour X
        X = df[self.feature_names].values
        
        # Targets pour y (prédire médailles prochains JO)
        # On utilise une moyenne pondérée favorisant les performances récentes
        y = np.column_stack([
            df['avg_gold_per_olympics'] * df['recent_trend_factor'],
            df['avg_silver_per_olympics'] * df['recent_trend_factor'],
            df['avg_bronze_per_olympics'] * df['recent_trend_factor']
        ])
        
        print(f"   ✅ Features shape: {X.shape}")
        print(f"   ✅ Targets shape: {y.shape}")
        
        return X, y, df['country_name'].values, df['country_code'].values
    
    def train_models(self):
        """Entraîner les modèles avec les VRAIES données MySQL"""
        print("\n" + "="*60)
        print("  ENTRAINEMENT ML AVEC DONNEES REELLES ALWAYSDATA")
        print("="*60 + "\n")
        
        # Charger les données MySQL
        df = self.load_data_from_mysql()
        
        # Préparer les features
        X, y, country_names, country_codes = self.prepare_features(df)
        
        # Split données
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Normaliser les features
        print("\n🔧 Normalisation des features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # === ENTRAINEMENT LINEAR REGRESSION ===
        print("\n📈 Entrainement Linear Regression...")
        self.linear_model = LinearRegression()
        self.linear_model.fit(X_train_scaled, y_train)
        
        y_pred_lr = self.linear_model.predict(X_test_scaled)
        mae_lr = mean_absolute_error(y_test, y_pred_lr)
        rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
        r2_lr = r2_score(y_test, y_pred_lr)
        
        print(f"   MAE: {mae_lr:.2f}")
        print(f"   RMSE: {rmse_lr:.2f}")
        print(f"   R² Score: {r2_lr:.3f}")
        
        # === ENTRAINEMENT RANDOM FOREST ===
        print("\n🌲 Entrainement Random Forest...")
        self.rf_model = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.rf_model.fit(X_train_scaled, y_train)
        
        y_pred_rf = self.rf_model.predict(X_test_scaled)
        mae_rf = mean_absolute_error(y_test, y_pred_rf)
        rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
        r2_rf = r2_score(y_test, y_pred_rf)
        
        print(f"   MAE: {mae_rf:.2f}")
        print(f"   RMSE: {rmse_rf:.2f}")
        print(f"   R² Score: {r2_rf:.3f}")
        
        # Feature importance
        print("\n📊 Feature Importance (Random Forest):")
        importances = self.rf_model.feature_importances_
        for name, importance in sorted(zip(self.feature_names, importances), 
                                      key=lambda x: x[1], reverse=True):
            print(f"   {name:<30} {importance:.3f}")
        
        return {
            'linear_regression': {'mae': mae_lr, 'rmse': rmse_lr, 'r2': r2_lr},
            'random_forest': {'mae': mae_rf, 'rmse': rmse_rf, 'r2': r2_rf}
        }
    
    def predict_paris_2024(self, country_code):
        """
        Prédire les médailles pour Paris 2024 pour un pays
        Utilise les VRAIES données historiques
        """
        if not self.linear_model or not self.rf_model:
            raise Exception("Les modeles doivent etre entraines d'abord")
        
        # Charger les données du pays depuis MySQL
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            m.country_name,
            m.country_code,
            COUNT(DISTINCT h.game_slug) as olympics_participated,
            COUNT(*) as total_medals,
            SUM(CASE WHEN m.medal_type = 'GOLD' THEN 1 ELSE 0 END) as gold_medals,
            SUM(CASE WHEN m.medal_type = 'SILVER' THEN 1 ELSE 0 END) as silver_medals,
            SUM(CASE WHEN m.medal_type = 'BRONZE' THEN 1 ELSE 0 END) as bronze_medals
        FROM medals m
        JOIN hosts h ON m.slug_game = h.game_slug
        WHERE m.country_code = %s
        GROUP BY m.country_name, m.country_code
        """
        
        cursor.execute(query, (country_code,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return None
        
        # Médailles récentes
        recent_query = """
        SELECT COUNT(*) as recent_medals
        FROM medals m
        JOIN hosts h ON m.slug_game = h.game_slug
        WHERE h.game_year >= 2012 AND m.country_code = %s
        """
        cursor.execute(recent_query, (country_code,))
        recent_medals = cursor.fetchone()[0]
        
        conn.close()
        
        # Créer les features
        olympics = result[2]
        total = result[3]
        gold = result[4]
        silver = result[5]
        bronze = result[6]
        
        avg_medals = total / olympics
        features = np.array([[
            gold / olympics,
            silver / olympics,
            bronze / olympics,
            olympics,
            total,
            gold / total,
            recent_medals / (avg_medals * 3 + 1),
            1 - abs((gold - silver - bronze) / total)
        ]])
        
        # Normaliser et prédire
        features_scaled = self.scaler.transform(features)
        
        lr_pred = self.linear_model.predict(features_scaled)[0]
        rf_pred = self.rf_model.predict(features_scaled)[0]
        
        # Moyenne des deux modèles (ensemble)
        ensemble_pred = (lr_pred + rf_pred) / 2
        
        return {
            'country_name': result[0],
            'country_code': country_code,
            'predicted_gold': int(round(ensemble_pred[0])),
            'predicted_silver': int(round(ensemble_pred[1])),
            'predicted_bronze': int(round(ensemble_pred[2])),
            'predicted_total': int(round(sum(ensemble_pred))),
            'model_confidence': 'high' if olympics > 15 else 'medium',
            'data_source': 'MySQL AlwaysData - Real Historical Data'
        }
    
    def predict_top_countries(self, limit=25):
        """Prédictions pour les top pays"""
        print(f"\n🏆 Generation des predictions pour le TOP {limit} pays...")
        
        # Charger les top pays depuis MySQL
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT DISTINCT country_code
        FROM medals
        WHERE country_code IS NOT NULL
        GROUP BY country_code
        ORDER BY COUNT(*) DESC
        LIMIT %s
        """
        cursor.execute(query, (limit,))
        top_countries = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        predictions = []
        for code in top_countries:
            pred = self.predict_paris_2024(code)
            if pred:
                predictions.append(pred)
        
        # Trier par total prédit
        predictions.sort(key=lambda x: x['predicted_total'], reverse=True)
        
        print(f"\n✅ Predictions TOP {len(predictions)} generees avec donnees REELLES MySQL")
        return predictions
    
    def save_models(self, directory='./models_mysql'):
        """Sauvegarder les modèles entraînés"""
        os.makedirs(directory, exist_ok=True)
        
        joblib.dump(self.linear_model, f'{directory}/linear_model_mysql.pkl')
        joblib.dump(self.rf_model, f'{directory}/random_forest_model_mysql.pkl')
        joblib.dump(self.scaler, f'{directory}/scaler_mysql.pkl')
        
        print(f"\n✅ Modeles sauvegardes dans {directory}/")
    
    def load_models(self, directory='./models_mysql'):
        """Charger les modèles sauvegardés"""
        self.linear_model = joblib.load(f'{directory}/linear_model_mysql.pkl')
        self.rf_model = joblib.load(f'{directory}/random_forest_model_mysql.pkl')
        self.scaler = joblib.load(f'{directory}/scaler_mysql.pkl')
        
        print(f"✅ Modeles charges depuis {directory}/")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  OLYMPIC ML PREDICTOR - MYSQL ALWAYSDATA VERSION")
    print("="*60)
    
    # Créer et entraîner le modèle
    predictor = OlympicPredictorMySQL()
    
    # Entraîner
    metrics = predictor.train_models()
    
    # Sauvegarder
    predictor.save_models()
    
    # Prédictions
    predictions = predictor.predict_top_countries(25)
    
    # Afficher TOP 10
    print("\n" + "="*60)
    print("  PREDICTIONS PARIS 2024 - TOP 10")
    print("="*60)
    for i, pred in enumerate(predictions[:10], 1):
        print(f"{i:2d}. {pred['country_name']:<25} "
              f"{pred['predicted_gold']:2d}🥇  "
              f"{pred['predicted_silver']:2d}🥈  "
              f"{pred['predicted_bronze']:2d}🥉  "
              f"Total: {pred['predicted_total']:2d}")
    
    # Sauvegarder les prédictions
    with open('predictions_paris_2024_mysql.json', 'w', encoding='utf-8') as f:
        json.dump(predictions, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Predictions sauvegardees dans predictions_paris_2024_mysql.json")
    print("\n" + "="*60)
    print("  ENTRAINEMENT TERMINE AVEC DONNEES REELLES MYSQL")
    print("="*60 + "\n")
