import sqlite3
import os
# Check if the directory exists, if not create it
os.makedirs('../data', exist_ok=True)

conn= sqlite3.connect('../data/articles.db')

cursor=conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles(
               
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT,
               content TEXT,
               summary TEXT,
               url TEXT,
               date TEXT)
            ''')

conn.commit()
conn.close()
