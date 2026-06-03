import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin

BASE = "https://roxiestreams.info"

CATEGORIES = [
    "soccer",
    "mlb",
    "nba",
    "nfl",
    "nhl",
    "fighting",
    "motorsports"
]

DOMAINS = [
    "formaturamaxi.com.br",
    "sandhost.qzz.io",
    "thelistener.pk"
]

SUBDOMAINS = ["601", "daffodil"]

headers = {"User-Agent": "Mozilla/5.0"}


# 🔥 витягуємо ВСІ можливі stream keys
def extract_streams(html):
    streams = set()

    # JS pattern
    streams.update(re.findall(r"getRandomStream\('([^']+\.m3u8)'", html))

    # прямі згадки
    streams.update(re.findall(r'([a-zA-Z0-9_-]+\.m3u8)', html))

    return list(streams)


# 🔥 НЕ перевіряємо через requests (це була помилка)
def build_streams(stream_key):
    urls = []

    for sub in SUBDOMAINS:
        for dom in DOMAINS:
            urls.append(f"https://{sub}.{dom}/{stream_key}")

    return urls


def parse_category(cat):
    url = f"{BASE}/{cat}"
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    # ❗ ВАЖЛИВО: НЕ фільтр "-streams"
    links = soup.select("a[href*='streams']")

    results = []

    for a in links:
        try:
            title = a.get_text(strip=True)
            page = urljoin(BASE, a["href"])

            r2 = requests.get(page, headers=headers, timeout=15)
            html = r2.text

            stream_keys = extract_streams(html)

            all_streams = []

            for key in stream_keys:
                all_streams.extend(build_streams(key))

            results.append({
                "title": title,
                "page": page,
                "streams": all_streams
            })

        except:
            continue

    return results


all_data = {}

for c in CATEGORIES:
    print("[INFO]", c)
    all_data[c] = parse_category(c)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print("DONE JSON")
