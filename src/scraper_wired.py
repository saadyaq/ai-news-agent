import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import time
import textwrap

# Préparation du répertoire
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Headers pour le scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

BASE_URL = "https://www.wired.com"

# 🔎 Étape 1 : Extraction des liens d’articles
def fetch_wired_article_links():
    response = requests.get(f"{BASE_URL}/most-recent/", headers=headers)
    if response.status_code != 200:
        print("[!] Échec du chargement de la page Wired.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        title = tag.get_text(strip=True)

        if href.startswith("/story/") and len(title) > 30:
            full_url = BASE_URL + href
            links.append((title, full_url))

    unique_links = list(set(links))
    print(f"[✓] {len(unique_links)} liens extraits depuis Wired.")
    return unique_links

# 🔍 Étape 2 : Extraction du contenu de l'article
def extract_wired_article_content(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join(p.get_text(strip=True) for p in paragraphs)
        return content
    except Exception as e:
        print(f"[!] Erreur avec {url} : {e}")
        return ""

# 💾 Étape 3 : Sauvegarde dans la base de données SQLite
def save_articles_to_db(df, db_path=os.path.join(DATA_DIR, "articles.db")):
    conn = sqlite3.connect(db_path)
    df.to_sql("articles", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    print(f"[✓] {len(df)} articles Wired enregistrés dans la base de données.")

# 🚀 Étape 4 : Pipeline principal
def main():
    articles = []
    links = fetch_wired_article_links()

    for title, url in links:
        print(f"Scraping: {title}")
        content = extract_wired_article_content(url)
        time.sleep(1)

        if len(content.strip()) < 300:
            continue

        articles.append({
            "title": title,
            "url": url,
            "content": textwrap.fill(content, width=80),
            "date": pd.Timestamp.now().strftime("%Y-%m-%d")
        })

    if articles:
        df = pd.DataFrame(articles)
        save_articles_to_db(df)
    else:
        print("[!] Aucun article valide trouvé.")

if __name__ == "__main__":
    main()
    print("[✓] Scraping Wired terminé avec succès.")
