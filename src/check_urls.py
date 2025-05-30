import requests
from bs4 import BeautifulSoup

url = "https://techcrunch.com/category/technology/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

articles = []
for tag in soup.find_all("a", href=True):
    title = tag.get_text(strip=True)
    href = tag["href"]
    if href.startswith("https://techcrunch.com/") and len(title) > 30:
        articles.append((title, href))

print(f"{len(articles)} articles trouvés :\n")
for title, link in articles[:10]:
    print("-", title)
    print(" ", link)
