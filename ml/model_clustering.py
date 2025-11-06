# Clustering : regrouper les pays par performance
import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# === 1. Chargement du dataset préparé ===
DATA_PATH = "ml/output/dataset_prepared.csv"
OUTPUT_PATH = "ml/output/clusters.csv"

print("📥 Chargement du dataset pour clustering...")
df = pd.read_csv(DATA_PATH)
print(f"✅ {len(df)} lignes chargées depuis {DATA_PATH}")

# === 2. Préparation des données ===
# On ne garde que les colonnes pertinentes
features = df[["total_medals", "game_year", "season_encoded"]]

# Normalisation des données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# === 3. Détermination du nombre optimal de clusters (Elbow Method) ===
inertias = []
K_range = range(2, 10)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(7, 5))
plt.plot(K_range, inertias, marker="o")
plt.title("Méthode du coude pour déterminer le nombre optimal de clusters")
plt.xlabel("Nombre de clusters (k)")
plt.ylabel("Inertie (Within Sum of Squares)")
plt.grid(True)
plt.tight_layout()
plt.show()

# === 4. Choix du nombre de clusters (ajuste si besoin) ===
best_k = 4  # valeur ajustable selon le graphique du coude
print(f"📊 Nombre de clusters choisi : {best_k}")

# === 5. Application du clustering ===
kmeans = KMeans(n_clusters=best_k, random_state=42)
df["cluster"] = kmeans.fit_predict(X_scaled)

# === 6. Analyse rapide des clusters ===
summary = df.groupby("cluster")[["total_medals", "game_year"]].agg(["mean", "count"]).reset_index()
print("\n📈 Résumé des clusters :")
print(summary)

# === 7. Sauvegarde ===
df.to_csv(OUTPUT_PATH, index=False)
print(f"💾 Fichier avec les clusters sauvegardé dans {OUTPUT_PATH}")
