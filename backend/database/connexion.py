import os
import pymysql
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

# Lire les variables d'environnement
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_PORT = int(os.getenv("DB_PORT", 3306))

# Fonction de connexion
def get_connection():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE,
            port=DB_PORT
        )
        print("✅ Connexion réussie à la base de données MySQL !")
        return conn
    except Exception as e:
        print("❌ Erreur de connexion :", e)
        return None


# Test direct
if __name__ == "__main__":
    connexion = get_connection()
    if connexion:
        cursor = connexion.cursor()
        cursor.execute("SHOW DATABASES;")
        print("📦 Bases disponibles :", cursor.fetchall())
        connexion.close()
        print("🔒 Connexion fermée.")
