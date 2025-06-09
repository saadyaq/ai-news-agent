import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os

# 🔐 Chargement depuis les secrets (GitHub Actions ou .env)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

DB_PATH = "data/clean_articles.db"
TABLE_NAME = "cleaned_articles"

# 📤 Récupérer les résumés récents
def get_summaries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    cursor.execute(f"""
        SELECT title, summary, url FROM {TABLE_NAME}
        WHERE summary IS NOT NULL AND date >= ?
        ORDER BY date DESC
        LIMIT 10
    """, (since,))

    rows = cursor.fetchall()
    conn.close()
    return rows

# 📧 Envoyer le mail
def send_email(subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

    print("📬 Email envoyé avec succès.")

# ▶️ Pipeline d'envoi
if __name__ == "__main__":
    summaries = get_summaries()

    if not summaries:
        print("❌ Aucun résumé à envoyer.")
    else:
        content = ""
        for title, summary, url in summaries:
            content += f"📰 {title}\n{summary}\n🔗 {url}\n\n"

        send_email("🗞️ Résumés quotidiens AI News", content)
