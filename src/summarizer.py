import openai
import sqlite3
import pandas as pd
import time
from openai import OpenAI
from datetime import datetime, timedelta
import os

db_path = "../data/articles.db"
table_name = "cleaned_articles"

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
    print("OpenAI API key is set.")
else:
    print("OpenAI API key is not set.")
    client = OpenAI()

#Création du prompt

def build_prompt(content):
    return (
        "Voici un article de presse.Résume-le de manière professionnelle mais ajoute aussi d'autres infos sue le sujet fait comme si tu introduisais le sujet à quelqu'un avec un niveau intermédiaire,"
        "en mettant en avant les idées principales et en concluant par une ouverture ou un axe de réflexion : \n\n "
        f"{content}"
    )

#Récuperer les articles à résumer 

def get_articles_to_summarize(limit=10):

    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    cursor.execute(f"""
        SELECT id, content FROM {table_name}
        WHERE summary IS NULL
        AND date >= ?
        ORDER BY date DESC
        LIMIT ?
    """, (since, limit))

    results = cursor.fetchall()
    conn.close()
    return results

#Mettre à jour les résumés dans la base

def update_summary(article_id,summary):

    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    cursor.execute(f"""
                   UPDATE {table_name}
                   SET summary=?
                   WHERE id=?""",(summary,article_id))
    conn.commit()
    conn.close()

#Appel à l'API d'OPENAI

def generate_summary(content):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": build_prompt(content)}
            ],
            temperature=0.7,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[!] Erreur OpenAI : {e}")
        return None


#Pipeline principale 

def main():
    articles = get_articles_to_summarize()
    print(f"📰 {len(articles)} articles à résumer...\n")

    for article_id, content in articles:
        print(f"📄 Article ID {article_id}...")

        summary = generate_summary(content)
        if summary:
            update_summary(article_id, summary)
            print("✅ Résumé ajouté.\n")
        else:
            print("❌ Erreur, résumé ignoré.\n")

        time.sleep(1.5)  # Pause pour éviter de dépasser les limites API

if __name__ == "__main__":
    main()