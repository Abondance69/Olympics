import os

# 📂 Dossier racine du projet (OLYMPICS)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 📂 Dossier ML/output (là où se trouvent tes modèles)
OUTPUT_DIR = os.path.join(BASE_DIR, "ml", "output")

# 📄 Fichiers attendus dans ml/output/
BEST_MODEL_PATH = os.path.join(OUTPUT_DIR, "best_model.pkl")
METRICS_REPORT_PATH = os.path.join(OUTPUT_DIR, "metrics_report.json")

ATHLETE_MODEL_PATH = os.path.join(OUTPUT_DIR, "athlete_model.pkl")
ATHLETE_SCALER_PATH = os.path.join(OUTPUT_DIR, "athlete_scaler.pkl")
ATHLETE_METRICS_PATH = os.path.join(OUTPUT_DIR, "athlete_metrics.json")

# ✅ Optionnel (ce fichier peut venir du clustering)
CLUSTERS_CSV_PATH = os.path.join(OUTPUT_DIR, "clusters.csv")

# 🔒 Sécurité / CORS
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*")

# 🧠 Vérification utile
if __name__ == "__main__":
    print("BASE_DIR :", BASE_DIR)
    print("OUTPUT_DIR :", OUTPUT_DIR)
    print("BEST_MODEL_PATH existe :", os.path.exists(BEST_MODEL_PATH))
    print("ATHLETE_MODEL_PATH existe :", os.path.exists(ATHLETE_MODEL_PATH))
