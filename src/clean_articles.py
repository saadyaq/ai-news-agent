import pandas as pd
import sqlite3
import os
import re

# 📁 Créer dossier si besoin
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Bases
SOURCE_DB = os.path.join(DATA_DIR, "articles.db")
TARGET_DB = os.path.join(DATA_DIR, "clean_articles.db")

# 🧽 Nettoyage simple
def clean_text(text):
    if not isinstance(text, str):
        return ""
    return re.sub(r"\s+", " ", text).strip()

# 📤 Nettoyer + transférer
def clean_and_transfer():
    conn_src = sqlite3.connect(SOURCE_DB)
    df = pd.read_sql_query("SELECT * FROM articles", conn_src)
    conn_src.close()

    if df.empty:
        print("❌ Aucun article trouvé dans la base source.")
        return

    df = df.drop_duplicates(subset=["title", "url"])
    df = df[df["content"].str.len() > 300]

    df["title"] = df["title"].apply(clean_text)
    df["content"] = df["content"].apply(clean_text)
    df["summary"] = None
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    conn_tgt = sqlite3.connect(TARGET_DB)
    urls_existantes = pd.read_sql_query("SELECT url FROM cleaned_articles", conn_tgt)["url"].tolist()

    df_new = df[~df["url"].isin(urls_existantes)]

    if df_new.empty:
        print("✅ Aucun nouvel article à insérer.")
    else:
        df_new[["title", "content", "summary", "url", "date"]].to_sql(
            "cleaned_articles", conn_tgt, if_exists="append", index=False
        )
        print(f"[✓] {len(df_new)} articles nettoyés transférés dans clean_articles.db")

    conn_tgt.commit()
    conn_tgt.close()

if __name__ == "__main__":
    clean_and_transfer()
