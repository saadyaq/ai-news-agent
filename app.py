import subprocess 
import time

import os
print("📁 Dossier courant :", os.getcwd())

def run_script(path):
    print(f"\n🚀 Lancement de {path}...")
    result = subprocess.run(["python3", path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"[!] Erreur dans {path} :\n{result.stderr}")


def main():

    scripts = [
    "src/scraper_coindesk.py",
    "src/scraper_cnbc.py",
    "src/scraper_tc.py",
    "src/scraper_ft.py",
    "src/scraper_wired.py",
    "src/clean_articles.py",
    "src/summarizer.py",
    "src/send_email.py"
    ]

    for script in scripts:
        run_script(script)
        time.sleep(2)
        
    print("\n✅ Pipeline terminée avec succès.")

if __name__ == "__main__":
    main()
