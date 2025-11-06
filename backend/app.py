from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import sys
import os

# Ajouter le dossier parent au PYTHONPATH pour importer database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import (
    BEST_MODEL_PATH, METRICS_REPORT_PATH,
    ATHLETE_MODEL_PATH, ATHLETE_SCALER_PATH, ATHLETE_METRICS_PATH,
    CLUSTERS_CSV_PATH, ALLOWED_ORIGINS
)
from utils import safe_load_json, safe_load_model

# =========================================================
# 🚀 Initialisation de l’application Flask
# =========================================================
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})

# =========================================================
# 📦 Chargement des artefacts au démarrage
# =========================================================
country_model = safe_load_model(BEST_MODEL_PATH)         # Modèle médailles pays
metrics_report = safe_load_json(METRICS_REPORT_PATH)

athlete_model = safe_load_model(ATHLETE_MODEL_PATH)      # Modèle athlète
athlete_scaler = safe_load_model(ATHLETE_SCALER_PATH)
athlete_metrics = safe_load_json(ATHLETE_METRICS_PATH)

clusters_df = None
try:
    clusters_df = pd.read_csv(CLUSTERS_CSV_PATH)
except Exception:
    clusters_df = None


# =========================================================
# 🧩 Helpers
# =========================================================
def bad_request(msg: str, code: int = 400):
    return jsonify({"status": "error", "message": msg}), code


# =========================================================
# 💓 API Health check
# =========================================================
@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "models": {
            "country_medals": country_model is not None,
            "athlete": (athlete_model is not None and athlete_scaler is not None)
        },
        "resources": {
            "clusters": clusters_df is not None,
            "metrics": metrics_report is not None and athlete_metrics is not None
        }
    })


# =========================================================
# 🌍 1) Clusters pays
# =========================================================
@app.get("/api/countries/clusters")
def get_clusters():
    if clusters_df is None:
        return bad_request("clusters.csv introuvable dans ml/output.")
    data = clusters_df.to_dict(orient="records")
    return jsonify({"status": "ok", "count": len(data), "data": data})


# =========================================================
# 🥇 2) Prédiction médailles pays
# =========================================================
@app.post("/api/predict/medals")
def predict_medals():
    if country_model is None:
        return bad_request("Modèle pays/médailles introuvable (best_model.pkl).")

    payload = request.get_json(silent=True) or {}
    required = ["country_name", "game_year", "game_season"]
    missing = [k for k in required if k not in payload]
    if missing:
        return bad_request(f"Champs manquants: {missing}")

    try:
        season_map = {"Summer": 0, "Winter": 1}
        X = pd.DataFrame([{
            "game_year": int(payload["game_year"]),
            "season_encoded": season_map.get(payload["game_season"], 0)
        }])

        y_pred = country_model.predict(X)[0]
        y_pred = int(np.maximum(0, round(float(y_pred))))
    except Exception as e:
        return bad_request(f"Erreur prédiction: {e}")

    return jsonify({
        "status": "ok",
        "input": payload,
        "prediction": {"total_medals": y_pred}
    })


# =========================================================
# 🧠 3) Prédiction athlète
# =========================================================
@app.post("/api/predict/athlete")
def predict_athlete():
    if athlete_model is None or athlete_scaler is None:
        return bad_request("Modèle athlète introuvable (athlete_model.pkl / scaler).")

    payload = request.get_json(silent=True) or {}

    games = payload.get("games_participations", 0)
    age = payload.get("age")
    year_birth = payload.get("athlete_year_birth")

    if age is None and year_birth is None:
        return bad_request("Fournis 'age' ou 'athlete_year_birth'.")

    if age is None and year_birth is not None:
        try:
            age = max(0, 2025 - int(year_birth))
        except Exception:
            return bad_request("athlete_year_birth invalide.")

    try:
        X = pd.DataFrame([{
            "athlete_age": int(age),
            "games_participations": int(games)
        }])
        if hasattr(athlete_scaler, "feature_names_in_"):
            X = X[list(athlete_scaler.feature_names_in_)]

        X_scaled = athlete_scaler.transform(X)
        proba = float(athlete_model.predict_proba(X_scaled)[0][1])
        pred = int(proba >= 0.5)
    except Exception as e:
        return bad_request(f"Erreur prédiction athlète: {e}")

    return jsonify({
        "status": "ok",
        "input": payload,
        "prediction": {"will_win_medal": bool(pred), "probability": round(proba, 4)}
    })


# =========================================================
# 📈 4) Métriques modèles
# =========================================================
@app.get("/api/metrics")
def get_metrics():
    return jsonify({
        "status": "ok",
        "country_medals": metrics_report or {},
        "athlete": athlete_metrics or {}
    })


# =========================================================
# 🏟️ 5) API Jeux (hosts)
# =========================================================
@app.get("/api/games")
def get_games():
    from database.connexion import get_connection
    from sqlalchemy import create_engine

    conn = get_connection()
    engine = create_engine(
        f"mysql+pymysql://{conn.user.decode()}:{conn.password.decode()}@{conn.host}:{conn.port}/{conn.db.decode()}"
    )

    query = "SELECT game_name, game_year, game_season, game_location FROM hosts ORDER BY game_year DESC"
    df = pd.read_sql(query, engine)

    season = request.args.get("season")
    if season:
        df = df[df["game_season"].str.lower() == season.lower()]

    return jsonify({
        "status": "ok",
        "count": len(df),
        "data": df.to_dict(orient="records")
    })


# =========================================================
# 🥇 6) API Résultats
# =========================================================
@app.get("/api/results")
def get_results():
    from database.connexion import get_connection
    from sqlalchemy import create_engine

    conn = get_connection()
    engine = create_engine(
        f"mysql+pymysql://{conn.user.decode()}:{conn.password.decode()}@{conn.host}:{conn.port}/{conn.db.decode()}"
    )

    query = "SELECT country_name, discipline_title, medal_type, slug_game, event_title FROM results"
    df = pd.read_sql(query, engine)

    country = request.args.get("country")
    game = request.args.get("game")
    season = request.args.get("season")

    if country:
        df = df[df["country_name"].str.contains(country, case=False, na=False)]
    if game:
        df = df[df["slug_game"].str.contains(game, case=False, na=False)]
    if season:
        df = df[df["slug_game"].str.contains(season, case=False, na=False)]

    return jsonify({
        "status": "ok",
        "count": len(df),
        "data": df.head(50).to_dict(orient="records")
    })

@app.get("/api/athletes")
def get_athletes():
    from database.connexion import get_connection
    import pandas as pd
    from sqlalchemy import create_engine

    conn = get_connection()
    engine = create_engine(
        f"mysql+pymysql://{conn.user.decode()}:{conn.password.decode()}@{conn.host}:{conn.port}/{conn.db.decode()}"
    )

    query = """
        SELECT athlete_full_name, games_participations, athlete_year_birth
        FROM athletes
        ORDER BY games_participations DESC
    """
    df = pd.read_sql(query, engine)

    # Filtres
    year_birth = request.args.get("year_birth")
    games_participations = request.args.get("games_participations")

    if year_birth:
        try:
            df = df[df["athlete_year_birth"] == int(year_birth)]
        except:
            pass

    if games_participations:
        try:
            df = df[df["games_participations"] == int(games_participations)]
        except:
            pass

    # Limiter les résultats
    limit = request.args.get("limit", 100)
    try:
        df = df.head(int(limit))
    except:
        df = df.head(100)

    return jsonify({
        "status": "ok",
        "count": len(df),
        "data": df.to_dict(orient="records")
    })
# =========================================================
# 🚀 Lancement principal
# =========================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
