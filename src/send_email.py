import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime,timedelta
import os
#Config email

SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")



db_path="../data/articles.db"
table_name="cleaned_articles"

def get_summaries():

    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    since=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    cursor.execute(f"""
                   SELECT title,summary FROM {table_name}
                   WHEZRE summary IS NOT NULL and date >=?
                   ORDER BY date DESC""",(since,))
    
    articles=cursor.fetchall()
    conn.close()
    return articles


def send_email(summaries):

    if not summaries :
        print("Aucun résumé à envoyer.")
        return 
    
    body="📬 Résumé quotidien des articles: \n\n"
    for title, summary in summaries:

        body+=f"🔸 {title}\n{summary}\n\n" 
    
    msg=MIMEText(body,"plain","utf-8")
    msg["Subject"]=f"📰 Résumé du {datetime.now().strftime('%d/%m/%Y')}"
    msg["From"]=SENDER_EMAIL
    msg["To"]=RECIPIENT_EMAIL

    try:
        server= smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL,SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 Email envoyé avec succès !")
    except Exception as e :
        print(f"[!] Erreur lors de l'envoi de l'email : {e}")

if __name__=="__main__":
    summaries=get_summaries()
    send_email(summaries)