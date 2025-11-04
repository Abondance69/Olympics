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
# medals_df = medals_df.where(pd.notnull(medals_df), None)

# print(medals_df.head())

# for _, row in medals_df.iterrows():
#     sql = """
#         INSERT INTO medals (
#             discipline_title, slug_game, event_title, event_gender, medal_type,
#             participant_type, participant_title, athlete_url, athlete_full_name,
#             country_name, country_code, country_3_letter_code
#         )
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """
#     values = (
#         row["discipline_title"],
#         row["slug_game"],
#         row["event_title"],
#         row["event_gender"],
#         row["medal_type"],
#         row["participant_type"],
#         row["participant_title"],
#         row["athlete_url"],
#         row["athlete_full_name"],
#         row["country_name"],
#         row["country_code"],
#         row["country_3_letter_code"],
#     )
#     cursor.execute(sql, values)

# conn.commit()
# print(f"✅ {len(medals_df)} lignes de médailles insérées avec succès !")


# === 3. ATHLETES (JSON)
print("🏃‍♂️ Chargement des données Athlètes (JSON)...")

athletes_df = pd.read_json("data/olympic_athletes.json")
athletes_df = athletes_df[['athlete_full_name', 'gender', 'country_name']]
athletes_df = athletes_df.where(pd.notnull(athletes_df), None)

print(athletes_df.head())

for _, row in athletes_df.iterrows():
    sql = """
        INSERT INTO athletes (athlete_full_name, gender, country_name)
        VALUES (%s, %s, %s)
    """
    values = (
        row["athlete_full_name"],
        row["gender"],
        row["country_name"]
    )
    cursor.execute(sql, values)

conn.commit()
print(f"✅ {len(athletes_df)} athlètes insérés avec succès !")


# === 4. RESULTS (HTML)
# print("📊 Chargement des données Résultats (HTML)...")

# Lecture du tableau HTML
# results_list = pd.read_html("data/olympic_results.html")
# results_df = results_list[0]
# results_df.columns = results_df.columns.str.lower().str.replace(" ", "_")
# results_df = results_df.where(pd.notnull(results_df), None)

# print(results_df.head())

# for _, row in results_df.iterrows():
#     sql = """
#         INSERT INTO results (
#             discipline_title, event_title, slug_game, participant_type, medal_type,
#             athletes, rank_equal, rank_position, country_name, country_code,
#             country_3_letter_code, athlete_url, athlete_full_name, value_unit, value_type
#         )
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """

#     # Conversion du champ "athletes" (liste -> JSON)
#     athletes_json = None
#     if isinstance(row.get("athletes"), list):
#         athletes_json = json.dumps(row["athletes"], ensure_ascii=False)
#     else:
#         athletes_json = json.dumps([])

#     values = (
#         row.get("discipline_title"),
#         row.get("event_title"),
#         row.get("slug_game"),
#         row.get("participant_type"),
#         row.get("medal_type"),
#         athletes_json,
#         row.get("rank_equal"),
#         row.get("rank_position"),
#         row.get("country_name"),
#         row.get("country_code"),
#         row.get("country_3_letter_code"),
#         row.get("athlete_url"),
#         row.get("athlete_full_name"),
#         row.get("value_unit"),
#         row.get("value_type"),
#     )
#     cursor.execute(sql, values)

# conn.commit()
# print(f"✅ {len(results_df)} résultats insérés avec succès !")

# === Fermeture propre ===
cursor.close()
conn.close()
print("🏁 Importation complète terminée avec succès ! 🎉")
