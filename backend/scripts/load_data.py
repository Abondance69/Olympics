import pandas as pd
import json
from io import StringIO
from database.connexion import get_connection

# Connexion à la base
conn = get_connection()
cursor = conn.cursor()
print("✅ Connexion réussie à la base de données MySQL !")

# === 1. HOSTS (XML)
print("🌍 Chargement des données Hosts (XML)...")

with open("data/olympic_hosts.xml", "r", encoding="utf-8") as f:
    xml_data = f.read()

hosts_df = pd.read_xml(StringIO(xml_data))
print(hosts_df.head())

for _, row in hosts_df.iterrows():
    sql = """
        INSERT INTO hosts (game_slug, game_end_date, game_start_date, game_location, game_name, game_season, game_year)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        row["game_slug"],
        row["game_end_date"],
        row["game_start_date"],
        row["game_location"],
        row["game_name"],
        row["game_season"],
        row["game_year"],
    )
    cursor.execute(sql, values)

conn.commit()
print(f"✅ {len(hosts_df)} hôtes insérés avec succès !")


# === 2. MEDALS (EXCEL)
print("🥇 Chargement des données Médailles (Excel)...")

medals_df = pd.read_excel("data/olympic_medals.xlsx")

# 🔧 Remplacer les NaN par None pour éviter l’erreur MySQL
medals_df = medals_df.where(pd.notnull(medals_df), None)

print(medals_df.head())

for _, row in medals_df.iterrows():
    sql = """
        INSERT INTO medals (
            discipline_title, slug_game, event_title, event_gender, medal_type,
            participant_type, participant_title, athlete_url, athlete_full_name,
            country_name, country_code, country_3_letter_code
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        row["discipline_title"],
        row["slug_game"],
        row["event_title"],
        row["event_gender"],
        row["medal_type"],
        row["participant_type"],
        row["participant_title"],
        row["athlete_url"],
        row["athlete_full_name"],
        row["country_name"],
        row["country_code"],
        row["country_3_letter_code"],
    )
    cursor.execute(sql, values)

conn.commit()
print(f"✅ {len(medals_df)} lignes de médailles insérées avec succès !")



# === 3. ATHLETES (JSON)
print("🏃‍♂️ Chargement des données Athlètes (JSON)...")

import json

# Lis le fichier JSON brut
with open("data/olympic_athletes.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 🔍 Si c’est une liste d’objets
print(f"Type de data : {type(data)}")
print(f"Nombre d'éléments : {len(data)}")
print("Premier élément du JSON :")
print(json.dumps(data[0], indent=2, ensure_ascii=False))

# Ensuite, charge dans pandas pour voir la structure
import pandas as pd
athletes_df = pd.DataFrame(data)

print("Colonnes détectées :")
print(athletes_df.columns.tolist())

print("\nAperçu du DataFrame :")
print(athletes_df.head(10))



# === 3. ATHLETES (JSON)
print("🏃‍♂️ Chargement des données Athlètes (JSON)...")

import json
import math
import numpy as np
from database.connexion import get_connection

# Lecture du fichier JSON
with open("data/olympic_athletes.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Conversion en DataFrame
athletes_df = pd.DataFrame(data)
print(athletes_df.head())

# Fonction utilitaire pour nettoyer les NaN / float
def clean_value(v):
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    return v

# === Insertion par "chunks" (blocs de 5000 lignes)
chunk_size = 5000
chunks = np.array_split(athletes_df, math.ceil(len(athletes_df) / chunk_size))

total_inserted = 0
chunk_number = 1

for chunk in chunks:
    print(f"🚀 Insertion du chunk {chunk_number}/{len(chunks)}...")

    # Ouvre une nouvelle connexion à chaque bloc pour éviter le timeout
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in chunk.iterrows():
        sql = """
            INSERT INTO athletes (
                athlete_url,
                athlete_full_name,
                games_participations,
                first_game,
                athlete_year_birth,
                athlete_medals,
                bio
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = tuple(clean_value(row[col]) for col in [
            "athlete_url",
            "athlete_full_name",
            "games_participations",
            "first_game",
            "athlete_year_birth",
            "athlete_medals",
            "bio"
        ])
        cursor.execute(sql, values)

    conn.commit()
    cursor.close()
    conn.close()

    total_inserted += len(chunk)
    print(f"✅ Chunk {chunk_number} terminé ({total_inserted}/{len(athletes_df)})")
    chunk_number += 1

print(f"🎯 Import complet : {total_inserted} athlètes insérés avec succès !")




# === 4. RESULTS (HTML)
print("📊 Chargement des données Résultats (HTML)...")

import json
import math

# Lecture du tableau HTML
results_list = pd.read_html("data/olympic_results.html")
results_df = results_list[0]
results_df.columns = results_df.columns.str.lower().str.replace(" ", "_").str.strip()
results_df = results_df.where(pd.notnull(results_df), None)

print(f"✅ Fichier HTML chargé avec {len(results_df)} lignes.")
print(results_df.head())

# Fonction utilitaire
def clean_value(v):
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    return str(v).strip() if isinstance(v, str) else v

# Fonction sécurisée pour les données JSON
def safe_json(val):
    """Convertit proprement la colonne athletes en JSON valide"""
    try:
        if isinstance(val, list):
            return json.dumps(val, ensure_ascii=False)
        if isinstance(val, str) and val.strip().startswith("["):
            json.loads(val)  # vérifie que c’est bien un JSON
            return val
        return json.dumps([], ensure_ascii=False)
    except Exception:
        return json.dumps([], ensure_ascii=False)

# Insertion avec commits progressifs
batch_size = 1000
count = 0

for _, row in results_df.iterrows():
    sql = """
        INSERT INTO results (
            discipline_title,
            event_title,
            slug_game,
            participant_type,
            medal_type,
            athletes,
            rank_equal,
            rank_position,
            country_name,
            country_code,
            country_3_letter_code,
            athlete_url,
            athlete_full_name,
            value_unit,
            value_type
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    athletes_json = safe_json(row.get("athletes"))

    values = (
        clean_value(row.get("discipline_title")),
        clean_value(row.get("event_title")),
        clean_value(row.get("slug_game")),
        clean_value(row.get("participant_type")),
        clean_value(row.get("medal_type")),
        athletes_json,
        clean_value(row.get("rank_equal")),
        clean_value(row.get("rank_position")),
        clean_value(row.get("country_name")),
        clean_value(row.get("country_code")),
        clean_value(row.get("country_3_letter_code")),
        clean_value(row.get("athlete_url")),
        clean_value(row.get("athlete_full_name")),
        clean_value(row.get("value_unit")),
        clean_value(row.get("value_type")),
    )

    try:
        cursor.execute(sql, values)
        count += 1
    except Exception as e:
        print(f"⚠️ Erreur sur ligne {count}: {e}")

    # Commit tous les 1000
    if count % batch_size == 0:
        conn.commit()
        print(f"✅ {count} résultats insérés...")

# Dernier commit
conn.commit()
print(f"🎯 Import terminé avec succès ({count} lignes).")



# === Fermeture propre ===
cursor.close()
conn.close()
print("🏁 Importation complète terminée avec succès ! 🎉")
