import requests
from bs4 import BeautifulSoup
import re
import json
import time
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


# 🔥 витягує ВСІ можливі m3u8 з сторінки
def extract_all_streams(html):
    streams = set()

    patterns = [
        r"https?://[^\"'\s]+\.m3u8[^\"'\s]*",
        r"https?://[^\"'\s]+/index_[^\"'\s]+\.m3u8[^\"'\s]*",
        r"https?://[^\"'\s]+\.ts[^\"'\s]*"
    ]

    for p in patterns:
        found = re.findall(p, html)
        for f in found:
            streams.add(f)

    # 🔥 ловимо JS типу getRandomStream('mlb.m3u8')
    js = re.findall(r"getRandomStream\('([^']+)'\)", html)
    for j in js:
        streams.add(j)

    return list(streams)


def get_streams_from_page(url):
    try:
        r = requests.get(url, headers=headers, timeout=15)
        return extract_all_streams(r.text)
    except:
        return []


def parse_category(cat):
    url = f"{BASE}/{cat}"
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    # 🔥 берем ВСІ лінки, не тільки streams
    links = soup.select("a[href]")

    for a in links:
        href = a.get("href")

        if not href:
            continue

        # тільки сторінки матчів
        if "-streams-" not in href:
            continue

        full_url = urljoin(BASE, href)
        title = a.text.strip() or "Unknown"

        print(f"[{cat}] parsing: {title}")

        streams = get_streams_from_page(full_url)

        # ❌ якщо нічого не знайдено
        if not streams:
            print("   -> NO STREAM FOUND")
            results.append({
                "title": title,
                "page": full_url,
                "streams": []
            })
            continue

        results.append({
            "title": title,
            "page": full_url,
            "streams": streams   # 🔥 ВСІ стріми, не один
        })

        time.sleep(0.3)

    return results


all_data = {}

for c in CATEGORIES:
    print(f"\n[INFO] {c}")
    all_data[c] = parse_category(c)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print("\nDONE JSON")
