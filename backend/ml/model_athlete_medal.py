# Prédire les athlètes susceptibles de gagner une médaille
import pandas as pd
import numpy as np
import os
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
from sqlalchemy import create_engine

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.connexion import get_connection

# === 1. Chargement des données ===
def load_athletes_data():
    conn = get_connection()
    engine = create_engine(
        f"mysql+pymysql://{conn.user.decode()}:{conn.password.decode()}@{conn.host}:{conn.port}/{conn.db.decode()}"
    )

    print("📥 Chargement de la table athletes depuis la base MySQL...")
    athletes = pd.read_sql("SELECT * FROM athletes", engine)
    print(f"✅ {len(athletes)} lignes chargées depuis la table athletes")

    return athletes


# === 2. Préparation du dataset ===
def prepare_dataset(df):
    # Création d'une variable cible (1 = a une médaille, 0 = aucune)
    df["has_medal"] = df["athlete_medals"].notnull().astype(int)

    # Nettoyage et sélection des variables utiles
    df["athlete_year_birth"] = pd.to_numeric(df["athlete_year_birth"], errors="coerce")
    df["games_participations"] = pd.to_numeric(df["games_participations"], errors="coerce")
    df["athlete_medals"] = df["athlete_medals"].fillna("0")

    # On enlève les lignes sans âge ni participation
    df = df.dropna(subset=["athlete_year_birth", "games_participations"])

    # Création d'une variable "age_approx" basée sur l'année du premier jeu
    current_year = 2024
    df["athlete_age"] = current_year - df["athlete_year_birth"]

    features = df[["games_participations", "athlete_age"]]
    target = df["has_medal"]

    return features, target


# === 3. Entraînement du modèle ===
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)

    # Évaluation
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print("\n📊 Évaluation du modèle :")
    print(f"✅ Accuracy : {acc:.3f}")
    print(f"✅ Précision : {prec:.3f}")
    print(f"✅ Rappel : {rec:.3f}")
    print(f"✅ F1-score : {f1:.3f}")
    print("\nMatrice de confusion :")
    print(cm)

    return model, scaler, {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1}


# === 4. Sauvegarde du modèle et des métriques ===
def save_outputs(model, scaler, metrics):
    OUTPUT_DIR = "ml/output"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    joblib.dump(model, os.path.join(OUTPUT_DIR, "athlete_model.pkl"))
    joblib.dump(scaler, os.path.join(OUTPUT_DIR, "athlete_scaler.pkl"))

    with open(os.path.join(OUTPUT_DIR, "athlete_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)

    print("\n💾 Modèle sauvegardé sous ml/output/athlete_model.pkl")
    print("💾 Scaler sauvegardé sous ml/output/athlete_scaler.pkl")
    print("💾 Métriques sauvegardées sous ml/output/athlete_metrics.json")


# === 5. Pipeline complet ===
if __name__ == "__main__":
    df = load_athletes_data()
    X, y = prepare_dataset(df)
    model, scaler, metrics = train_model(X, y)
    save_outputs(model, scaler, metrics)
    print("\n🏁 Entraînement terminé avec succès !")
