import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import time


# Check if the directory exists, if not create it
os.makedirs('../data', exist_ok=True)

#Function to scrape articles 

def scrape_article_content(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tester plusieurs sélecteurs
        paragraphs = soup.select('div.article-content-wrapper p')
        if not paragraphs:
            print(f"Aucun contenu trouvé pour {url}")
            return ""

        content = ' '.join([p.get_text(strip=True) for p in paragraphs])
        return content
    except Exception as e:
        print(f"Erreur lors du scraping de l’article {url}: {e}")
        return ""


def scrape_coin_desk():
    url = "https://www.coindesk.com/"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for item in soup.select('div.col-span-1 a'):
        title = item.get_text(strip=True)
        link = item['href']

        # Skip empty titles
        if not title:
            continue

        # Fix full_url construction
        if str(link).startswith('http'):
            full_url = link
        else:
            full_url = f"https://www.coindesk.com{link}"

        print(f"Scraping {title}")
        try:
            content = scrape_article_content(full_url)
        except Exception as e:
            print(f"Error scraping {full_url}: {e}")
            continue

        time.sleep(1)

        articles.append({
            'title': title,
            'content': content,
            'summary': None,
            'url': full_url,
            'date': pd.Timestamp.now().strftime("%Y-%m-%d")
        })

    if articles:
        return pd.DataFrame(articles)
    else:
        print("Aucun article trouvé.")
        return pd.DataFrame(columns=['title', 'content', 'summary', 'url', 'date'])

def save_articles_to_db(df):
    conn= sqlite3.connect('../data/articles.db')
    df.to_sql("articles", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    print("Articles saved to database.")

def main():

    df_coindesk=scrape_coin_desk()

    print(df_coindesk.head())
    save_articles_to_db(df_coindesk)
    print("Scraping completed.")
if __name__== "__main__":
    main()



