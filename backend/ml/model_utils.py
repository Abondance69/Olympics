# Fonctions communes : évaluation, sauvegarde
import joblib
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, confusion_matrix

def save_model(model, path):
    joblib.dump(model, path)
    print(f"✅ Modèle sauvegardé : {path}")

def evaluate_regression(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"📊 MAE = {mae:.3f} | R² = {r2:.3f}")
    return mae, r2

def evaluate_classification(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    print(f"🎯 Accuracy = {acc:.3f}")
    print("🧩 Matrice de confusion :")
    print(cm)
    return acc, cm
