import openai
import sqlite3
import time
from datetime import datetime, timedelta
import os

# 🔐 Clé API via variable d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")

DB_PATH = "/home/saadyaq/SE/Python/ai-news-agent/data/clean_articles.db"
TABLE_NAME = "cleaned_articles"

if openai.api_key:
    print("🔑 OpenAI API key is set.")
else:
    print("❌ OpenAI API key is NOT set.")

# 📋 Prompt pour le résumé
def build_prompt(content):
    return (
        "Voici un article de presse. Résume-le en français de manière claire, concise et professionnelle, "
        "en mettant en avant les idées principales et en concluant par une ouverture :\n\n"
        f"{content}"
    )

# 📥 Récupérer les articles sans résumé, publiés dans les dernières 24h
def get_articles_to_summarize(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    cursor.execute(f"""
        SELECT id, content FROM {TABLE_NAME}
        WHERE summary IS NULL AND date >= ?
        ORDER BY date DESC
        LIMIT ?
    """, (since, limit))

    rows = cursor.fetchall()
    conn.close()
    return rows

# 🧠 Appel à l'API
def generate_summary(content):
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": build_prompt(content)}],
            temperature=0.7,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[!] Erreur OpenAI : {e}")
        return None

# ✏️ Mise à jour du résumé
def update_summary(article_id, summary):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE {TABLE_NAME}
        SET summary = ?
        WHERE id = ?
    """, (summary, article_id))
    conn.commit()
    conn.close()

# ▶️ Pipeline principale
def main():
    articles = get_articles_to_summarize()
    print(f"📰 {len(articles)} articles à résumer...\n")

    for article_id, content in articles:
        print(f"📄 Article ID {article_id}")
        summary = generate_summary(content)
        if summary:
            update_summary(article_id, summary)
            print("✅ Résumé ajouté.\n")
        else:
            print("❌ Résumé ignoré.\n")
        time.sleep(1.5)

if __name__ == "__main__":
    main()
