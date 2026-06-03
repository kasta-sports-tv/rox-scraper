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

SUBDOMAIN = "601"

headers = {"User-Agent": "Mozilla/5.0"}


def extract_streams(html):
    return list(set(re.findall(r'[a-zA-Z0-9_-]+\.m3u8', html)))


def check_stream(stream):
    for d in DOMAINS:
        url = f"https://{SUBDOMAIN}.{d}/{stream}"

        try:
            r = requests.get(url, timeout=5)

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
            streams = extract_streams(r2.text)

            final_streams = []

            for s in streams:
                real = check_stream(s)
                if real:
                    final_streams.append(real)

            results.append({
                "title": title,
                "page": page,
                "streams": final_streams
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
