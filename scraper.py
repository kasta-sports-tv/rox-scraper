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

headers = {
    "User-Agent": "Mozilla/5.0"
}


def extract_streams(html):
    """
    витягує ТІЛЬКИ повні m3u8 (https://....m3u8)
    """
    return list(set(
        re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', html)
    ))


def parse_category(cat):
    url = f"{BASE}/{cat}"
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.select("a[href*='-streams-']")

    results = []

    for a in links:
        try:
            title = a.get_text(strip=True)
            page = urljoin(BASE, a["href"])

            r2 = requests.get(page, headers=headers, timeout=15)
            streams = extract_streams(r2.text)

            results.append({
                "title": title,
                "page": page,
                "streams": streams
            })

        except Exception as e:
            print(f"[ERROR] {page} -> {e}")
            continue

    return results


all_data = {}

for c in CATEGORIES:
    print(f"[INFO] {c}")
    all_data[c] = parse_category(c)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print("DONE JSON")
