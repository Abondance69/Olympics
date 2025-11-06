# ============================================
# 🥇 Prédiction du nombre de médailles (par pays)
# ============================================
import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# === 1. Chargement des données ===
DATA_PATH = "ml/output/dataset_prepared.csv"
OUTPUT_DIR = "ml/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("📥 Chargement du dataset...")
df = pd.read_csv(DATA_PATH)
print(f"✅ {len(df)} lignes chargées depuis {DATA_PATH}")

# === 2. Préparation des features ===
df = df.dropna(subset=["total_medals", "country_name"])

# Encodage du pays
encoder = LabelEncoder()
df["country_encoded"] = encoder.fit_transform(df["country_name"])

# Sélection des features
X = df[["country_encoded", "game_year", "season_encoded"]]
y = df["total_medals"]

# === 3. Split train/test ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === 4. Définition des modèles ===
models = {
    "LinearRegression": LinearRegression(),
    "DecisionTree": DecisionTreeRegressor(random_state=42),
    "RandomForest": RandomForestRegressor(random_state=42)
}

results = {}

# === 5. Entraînement et évaluation ===
for name, model in models.items():
    print(f"\n🚀 Entraînement du modèle : {name}")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    results[name] = {"MAE": mae, "RMSE": rmse, "R2": r2}
    print(f"✅ {name} → MAE={mae:.2f}, RMSE={rmse:.2f}, R2={r2:.3f}")

# === 6. Sélection du meilleur modèle ===
best_model_name = max(results, key=lambda k: results[k]["R2"])
best_model = models[best_model_name]
print(f"\n🏆 Meilleur modèle : {best_model_name} avec R²={results[best_model_name]['R2']:.3f}")

# === 7. Sauvegarde du modèle et du LabelEncoder ===
joblib.dump(best_model, os.path.join(OUTPUT_DIR, "best_model.pkl"))
joblib.dump(encoder, os.path.join(OUTPUT_DIR, "country_encoder.pkl"))

# === 8. Sauvegarde du rapport de métriques ===
with open(os.path.join(OUTPUT_DIR, "metrics_report.json"), "w") as f:
    json.dump(results, f, indent=4)

print("💾 Modèle sauvegardé dans:", os.path.join(OUTPUT_DIR, "best_model.pkl"))
print("💾 Encodage des pays sauvegardé dans:", os.path.join(OUTPUT_DIR, "country_encoder.pkl"))
print("📊 Rapport des métriques enregistré dans:", os.path.join(OUTPUT_DIR, "metrics_report.json"))
