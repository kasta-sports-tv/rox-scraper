import requests
from bs4 import BeautifulSoup
import re
import json
import time

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


def extract_m3u8(html):
    m3u8 = re.findall(r"https?://[^\s'\"<>]+\.m3u8[^\s'\"<>]*", html)
    if m3u8:
        return m3u8[0]

    return None


def get_stream(url):
    try:
        r = requests.get(url, headers=headers, timeout=15)
        return extract_m3u8(r.text)
    except:
        return None


def parse_category(cat):
    url = f"{BASE}/{cat}"
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for a in soup.select("a[href]"):
        href = a.get("href")

        if not href:
            continue

        if "-streams-" not in href:
            continue

        full_url = href if href.startswith("http") else BASE + href
        title = a.text.strip() or "Unknown"

        print("[+] ", title)

        stream = get_stream(full_url)

        results.append({
            "title": title,
            "stream": stream
        })

        time.sleep(0.3)

    return results


all_data = {}

for c in CATEGORIES:
    print("\nCAT:", c)
    all_data[c] = parse_category(c)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print("DONE")
