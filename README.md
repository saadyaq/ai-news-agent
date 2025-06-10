# AI News Agent

AI News Agent is an automated pipeline that collects technology news, cleans the content and summarizes it using OpenAI. Summaries are then emailed daily. The project includes scrapers for several major outlets and a basic Streamlit dashboard.

## Features
- **Scraping**: TechCrunch, CNBC, CoinDesk, Financial Times and Wired articles are scraped daily.
- **Cleaning**: Articles are filtered and deduplicated before being stored in a SQLite database.
- **Summarization**: Recent articles are summarized via the OpenAI API.
- **Email Digest**: Summaries from the last 24 hours are sent as an email report.
- **Automation**: A GitHub Actions workflow executes the entire pipeline every morning.

## Requirements
- Python 3.10+
- The packages listed in [`requirements.txt`](requirements.txt)
- ChromeDriver (for the CoinDesk scraper via Selenium)

## Quick Start
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set environment variables**
   - `OPENAI_API_KEY` – API key for summarization
   - `SENDER_EMAIL` and `EMAIL_APP_PASSWORD` – credentials used to send the digest
   - `RECIPIENT_EMAIL` – address receiving the digest
3. **Initialize the databases**
   ```bash
   python src/create_art_db.py
   python src/create_db.py
   ```
4. **Run the pipeline**
   ```bash
   python app.py
   ```

## Pipeline Stages
1. **Scrapers** (`src/scraper_*.py`)
   - Each script fetches the latest articles from its respective source and stores them in `data/articles.db`.
2. **Cleaning** (`src/clean_articles.py`)
   - Deduplicates, cleans text and transfers new articles to `data/clean_articles.db`.
3. **Summarization** (`src/summarizer.py`)
   - Generates short French summaries for articles from the last 24 hours.
4. **Email** (`src/send_email.py`)
   - Builds an HTML email containing the summaries and sends it to the recipient.

These steps are executed sequentially by [`app.py`](app.py).

## Automation
The workflow in [`.github/workflows/daily-pipeline.yml`](.github/workflows/daily-pipeline.yml) runs the pipeline at 06:00 Paris time (using the `Europe/Paris` timezone) each day. The required secrets must be set in the repository for it to send emails and call the OpenAI API. Ensure the workflow file resides on your default branch so that the schedule triggers correctly.

## Data
All article data and summaries are stored in the `data/` directory:
- `articles.db` – raw scraped articles
- `clean_articles.db` – cleaned articles with summaries

CSV exports (`articles_dump.csv`, `articles_cleaned.csv`) are provided for convenience.

## Directory Structure
```
├── app.py               # orchestrates the pipeline
├── src/                 # scraping and utility scripts
├── data/                # SQLite databases and CSV exports
├── streamlit_app/       # (placeholder) dashboard
└── .github/workflows/   # GitHub Actions workflow
```

## License
This project is released under the MIT License.

## Author
Saad Yaqine
