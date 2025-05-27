from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://www.coindesk.com/markets/")
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")

# 🔥 Nouveau sélecteur basé sur les classes
links = []
for a in soup.select("a.text-color-charcoal-900.mb-4.hover\\:underline"):
    href = a.get("href")
    text = a.get_text(strip=True)
    if href and text and len(text) > 20 and href.startswith("/"):
        full_url = "https://www.coindesk.com" + href
        links.append((text, full_url))

driver.quit()

print(f"{len(links)} articles CoinDesk détectés :\n")
for title, url in links[:10]:
    print("-", title)
    print(" ", url)
