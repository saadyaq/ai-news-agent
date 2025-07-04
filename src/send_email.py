import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from urllib.parse import urlparse

import re

import os

# 🔐 Chargement depuis les secrets (GitHub Actions ou .env)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "clean_articles.db")
TABLE_NAME = "cleaned_articles"


# 📤 Récupérer les résumés récents
def get_summaries(max_per_domain=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    cursor.execute(
        f"""
        SELECT title, summary, url FROM {TABLE_NAME}
        WHERE summary IS NOT NULL AND date >= ?
        ORDER BY date DESC
    """,
        (since,),
    )

    rows = cursor.fetchall()
    conn.close()

    grouped = {}
    for row in rows:
        domain = urlparse(row[2]).netloc
        grouped.setdefault(domain, [])
        if len(grouped[domain]) < max_per_domain:
            grouped[domain].append(row)

    limited_rows = []
    for domain_rows in grouped.values():
        limited_rows.extend(domain_rows)

    return limited_rows



# ✂️ S'assurer que chaque résumé se termine par une phrase complète
def complete_sentence(text: str) -> str:
    """Trim trailing partial sentence if summary appears cut."""
    text = text.strip()
    if not text or text[-1] in ".!?\u2026":
        return text

    # Chercher la dernière ponctuation forte
    match = re.search(r"[.!?\u2026](?!.*[.!?\u2026])", text)
    if match:
        return text[: match.end()]
    return text



# 📧 Envoyer le mail
def send_email(subject, html_body):
    """Send an email with HTML content."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    msg.attach(MIMEText(html_body, "html", "utf-8"))

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
        content = "<p>Bonjour,</p><p>Voici les résumés des dernières 24 heures :</p>"
        for i, (title, summary, url) in enumerate(summaries, 1):
            summary = complete_sentence(summary)
            content += (
                f"<hr><h3>{i}. {title}</h3>"
                f"<p>{summary}</p>"
                f"<p><a href='{url}'>Lire l'article</a></p>"
            )
        content += "<p>Bonne lecture,<br>L'équipe AI News</p>"
        send_email("🗞️ Résumés quotidiens AI News", content)
