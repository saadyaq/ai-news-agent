import requests
from bs4 import BeautifulSoup

url = "https://www.ft.com/technology"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.google.com/"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

links = []
for a in soup.find_all("a", href=True):
    href = a.get("href")   # type: ignore
    title = a.get_text(strip=True)
    if href and "/content/" in href and len(title) > 30:
        full_url = "https://www.coindesk.com" + str(href)
        links.append((title, full_url))

print(f"{len(links)} articles trouvés :\n")
for title, link in links[:5]:
    print("-", title)
    print(" ", link)