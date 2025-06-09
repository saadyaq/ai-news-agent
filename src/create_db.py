import os
import sqlite3

# Chemin absolu vers le dossier du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "clean_articles.db")

# Création du dossier si nécessaire
os.makedirs(DATA_DIR, exist_ok=True)

# Connexion à la base
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Création de la table
cursor.execute("DROP TABLE IF EXISTS cleaned_articles")
cursor.execute("""
CREATE TABLE cleaned_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    summary TEXT,
    url TEXT,
    date TEXT
)
""")

conn.commit()
conn.close()

print(f"✅ Base créée à : {DB_PATH}")
