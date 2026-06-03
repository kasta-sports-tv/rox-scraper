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

headers = {"User-Agent": "Mozilla/5.0"}


# 🔥 витягуємо ВСЕ що може бути m3u8
def extract_streams(html):
    found = set()

    # прямі
    found.update(re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', html))

    # getRandomStream('xxx.m3u8'
    found.update(re.findall(r"getRandomStream\('([^']+\.m3u8)'", html))

    # просто xxx.m3u8
    found.update(re.findall(r'([a-zA-Z0-9_-]+\.m3u8)', html))

    return list(found)


# 🔥 перевірка доменів (підбір РОБОЧОГО)
def resolve_stream(stream_path):
    for d in DOMAINS:
        for sub in ["601", "daffodil"]:
            url = f"https://{sub}.{d}/{stream_path}"

            try:
                r = requests.get(url, timeout=6)

                if r.status_code == 200 and "m3u8" in r.text:
                    return url

            except:
                continue

    return None


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
            html = r2.text

            streams_raw = extract_streams(html)

            resolved = []

            for s in streams_raw:
                real = resolve_stream(s)
                if real:
                    resolved.append(real)

            results.append({
                "title": title,
                "page": page,
                "streams": resolved
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
