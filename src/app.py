import subprocess 
import time


def run_script(name):
    print(f"\n🚀 Lancement de {name}...")
    result = subprocess.run(["python3", name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"[!] Erreur dans {name} :\n{result.stderr}")

def main():

    scripts = [
    "scraper_coindesk.py",
    "scrape_cnbc.py",
    "scrape_techcrunch.py",
    "scrape_wired.py",
    "clean_articles.py",
    "summarizer.py",
    "send_email.py"
    ]
    for script in scripts:
        run_script(script)
        time.sleep(2)
        
    print("\n✅ Pipeline terminée avec succès.")

if __name__ == "__main__":
    main()