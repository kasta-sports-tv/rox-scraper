import requests
from bs4 import BeautifulSoup
import re
import json

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

headers = {"User-Agent": "Mozilla/5.0"}


def extract_streams(html):
    """
    витягує ВСІ можливі m3u8 або path типу xxx.m3u8
    """
    links = re.findall(r'(https?://[^\s"\']+\.m3u8|[a-zA-Z0-9_-]+\.m3u8)', html)

    cleaned = []
    for l in links:
        if l not in cleaned:
            cleaned.append(l)

    return cleaned


def parse_category(cat):
    url = f"{BASE}/{cat}"
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.select("a[href*='-streams']")

    results = []

    for a in rows:
        try:
            title = a.text.strip()
            page = a["href"]

            r2 = requests.get(page, headers=headers, timeout=15)
            streams = extract_streams(r2.text)

            results.append({
                "title": title,
                "page": page,
                "streams": streams
            })

        except:
            continue

    return results


all_data = {}

for c in CATEGORIES:
    print(f"[INFO] {c}")
    all_data[c] = parse_category(c)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print("DONE JSON")
