import pandas as pd
from sqlalchemy import create_engine
from database.connexion import get_connection


def normalize_key(x):
    if isinstance(x, str):
        return x.strip().lower().replace(" ", "").replace("-", "")
    return x


def load_data():
    conn = get_connection()

    engine = create_engine(
        f"mysql+pymysql://{conn.user.decode()}:{conn.password.decode()}@{conn.host}:{conn.port}/{conn.db.decode()}"
    )

    print("🔄 Chargement des tables...")
    hosts = pd.read_sql("SELECT * FROM hosts", engine)
    athletes = pd.read_sql("SELECT * FROM athletes", engine)
    results = pd.read_sql("SELECT * FROM results", engine)
    medals = pd.read_sql("SELECT * FROM medals", engine)
    print("✅ Données chargées !")

    # Normalisation des clés
    results["slug_game_clean"] = results["slug_game"].apply(normalize_key)
    medals["slug_game_clean"] = medals["slug_game"].apply(normalize_key)
    hosts["game_slug_clean"] = hosts["game_slug"].apply(normalize_key)

    # === Fusion results + medals ===
    merged = results.merge(
        medals[["country_name", "slug_game_clean", "medal_type"]],
        on=["country_name", "slug_game_clean"],
        how="left",
        suffixes=("_results", "_medals")
    )

    # === Unifier les colonnes de médaille ===
    merged["medal_type"] = merged["medal_type_results"].combine_first(merged["medal_type_medals"])

    # === Fusion avec hosts ===
    merged = merged.merge(
        hosts[["game_slug_clean", "game_year", "game_season"]],
        left_on="slug_game_clean",
        right_on="game_slug_clean",
        how="left"
    )

    print(f"✅ Fusion réussie : {len(merged)} lignes après jointures")

    # Vérif
    if merged["medal_type"].isna().all():
        print("⚠️ Attention : toutes les valeurs de 'medal_type' sont NaN. Vérifie la correspondance des clés !")

    # === Agrégation ===
    dataset = (
        merged.groupby(["country_name", "game_year", "game_season"])["medal_type"]
        .count()
        .reset_index()
        .rename(columns={"medal_type": "total_medals"})
    )

    # Nettoyage
    dataset = dataset[dataset["game_year"].notna()]
    dataset["game_year"] = dataset["game_year"].astype(int)
    dataset["season_encoded"] = dataset["game_season"].map({"Summer": 0, "Winter": 1}).fillna(0)

    dataset.to_csv("ml/output/dataset_prepared.csv", index=False, encoding="utf-8")
    print(f"💾 Dataset fusionné sauvegardé ({len(dataset)} lignes) → ml/dataset_prepared.csv")

    return dataset


if __name__ == "__main__":
    df = load_data()
    print("\n🔍 Aperçu du dataset préparé :")
    print(df.head())
