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

HEADERS = {"User-Agent": "Mozilla/5.0"}

DOMAINS = [
    "formaturamaxi.com.br",
    "sandhost.qzz.io",
    "thelistener.pk"
]

SUBDOMAINS = ["601", "daffodil"]


def extract_keys(html):
    # бере тільки ключі типу fsp.m3u8, mlb3.m3u8
    return list(set(re.findall(r'[a-zA-Z0-9_-]+\.m3u8', html)))


def test_stream(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        return "#EXTM3U" in r.text
    except:
        return False


def find_working_stream(stream_key):
    # пробуємо як є (якщо це повний URL)
    if stream_key.startswith("http"):
        return stream_key

    # пробуємо всі комбінації, але ЗУПИНЯЄМОСЬ на першому робочому
    for sub in SUBDOMAINS:
        for dom in DOMAINS:
            url = f"https://{sub}.{dom}/{stream_key}"

            if test_stream(url):
                return url

    return None


def parse_category(cat):
    url = f"{BASE}/{cat}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.select("a[href*='-streams']")

    results = []

    for a in links:
        try:
            title = a.text.strip()
            page = a["href"]

            r2 = requests.get(page, headers=HEADERS, timeout=15)
            html = r2.text

            keys = extract_keys(html)

            streams = []
            for key in keys:
                stream = find_working_stream(key)
                if stream:
                    streams.append(stream)

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
