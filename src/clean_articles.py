import pandas as pd
import sqlite3
from bs4 import BeautifulSoup

def clean_articles(df):
    df=df.drop_duplicates(subset=['title','url']).reset_index(drop=True)
    df=df[df['content'].str.len()>300]

    return df

def load_articles(db_path="../data/articles.db"):
    conn=sqlite3.connect(db_path)
    df=pd.read_sql_query("SELECT * FROM articles",conn)
    conn.close()
    return df

def save_cleaned_to_db(df,db_path="../data/articles.db"):
    conn=sqlite3.connect(db_path)
    df.to_sql("cleaned_articles",conn,if_exists="replace",index=False)
    conn.commit()
    conn.close()
    print(f"[✓] {len(df)} articles nettoyés sauvegardés dans 'cleaned_articles'.")

if __name__=="__main__":
    df_raw=load_articles()
    df_cleaned=clean_articles(df_raw)
    save_cleaned_to_db(df_cleaned)