from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np

from backend.config import (
    BEST_MODEL_PATH, METRICS_REPORT_PATH,
    ATHLETE_MODEL_PATH, ATHLETE_SCALER_PATH, ATHLETE_METRICS_PATH,
    CLUSTERS_CSV_PATH, ALLOWED_ORIGINS
)
from backend.utils import safe_load_json, safe_load_model

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})

# === Chargement des artefacts au démarrage ===
country_model = safe_load_model(BEST_MODEL_PATH)         # Pipeline sklearn attendu
metrics_report = safe_load_json(METRICS_REPORT_PATH)

athlete_model = safe_load_model(ATHLETE_MODEL_PATH)      # Classif sklearn
athlete_scaler = safe_load_model(ATHLETE_SCALER_PATH)
athlete_metrics = safe_load_json(ATHLETE_METRICS_PATH)

clusters_df = None
try:
    clusters_df = pd.read_csv(CLUSTERS_CSV_PATH)
except Exception:
    clusters_df = None

# === Helpers de validation ===
def bad_request(msg: str, code: int = 400):
    return jsonify({"status": "error", "message": msg}), code

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

# =============== 1) Clusters pays ===============
@app.get("/api/countries/clusters")
def get_clusters():
    if clusters_df is None:
        return bad_request("clusters.csv introuvable dans ml/output.")
    # Retour simple : [{country_name, cluster, ...}, ...]
    data = clusters_df.to_dict(orient="records")
    return jsonify({"status": "ok", "count": len(data), "data": data})

# =============== 2) Prédiction médailles pays ===============
@app.post("/api/predict/medals")
def predict_medals():
    if country_model is None:
        return bad_request("Modèle pays/médailles introuvable (best_model.pkl).")

    payload = request.get_json(silent=True) or {}
    # On attend : country_name, game_year, game_season
    required = ["country_name", "game_year", "game_season"]
    missing = [k for k in required if k not in payload]
    if missing:
        return bad_request(f"Champs manquants: {missing}")

    try:
        X = pd.DataFrame([{
            "country_name": payload["country_name"],
            "game_year": int(payload["game_year"]),
            "game_season": payload["game_season"]
        }])
        # Le Pipeline doit gérer l'encodage en interne
        y_pred = country_model.predict(X)[0]
        # Si le modèle renvoie des float, arrondissons proprement
        y_pred = int(np.maximum(0, round(float(y_pred))))
    except Exception as e:
        return bad_request(f"Erreur prédiction: {e}")

    return jsonify({
        "status": "ok",
        "input": payload,
        "prediction": {"total_medals": y_pred}
    })

# =============== 3) Prédiction athlète ===============
@app.post("/api/predict/athlete")
def predict_athlete():
    if athlete_model is None or athlete_scaler is None:
        return bad_request("Modèle athlète introuvable (athlete_model.pkl / scaler).")

    payload = request.get_json(silent=True) or {}
    # On attend minimalement : games_participations et year_birth (ou age)
    # Optionnel: recent_medals, results_count etc. selon ton entraînement
    games = payload.get("games_participations", None)
    age = payload.get("age", None)
    year_birth = payload.get("athlete_year_birth", None)

    if age is None and year_birth is None:
        return bad_request("Fournis 'age' ou 'athlete_year_birth'.")

    if age is None and year_birth is not None:
        try:
            age = max(0, 2025 - int(year_birth))  # approx
        except Exception:
            return bad_request("athlete_year_birth invalide.")

    if games is None:
        games = 0

    try:
        X = pd.DataFrame([{"age": int(age), "games_participations": int(games)}])
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

# =============== 4) Métriques modèles ===============
@app.get("/api/metrics")
def get_metrics():
    return jsonify({
        "status": "ok",
        "country_medals": metrics_report or {},
        "athlete": athlete_metrics or {}
    })

if __name__ == "__main__":
    # Lancement direct (dev). En prod, utilise gunicorn/uvicorn.
    app.run(host="0.0.0.0", port=8000, debug=True)
