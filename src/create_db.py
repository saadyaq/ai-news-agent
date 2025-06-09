import sqlite3, os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("../data/clean_articles.db")
cursor = conn.cursor()

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
print("✅ Base 'clean_articles.db' créée avec table 'cleaned_articles'.")
