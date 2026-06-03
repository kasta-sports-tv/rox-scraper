import json

DOMAINS = []
SUBDOMAINS = []

# читаємо домени
with open("domainsz29.txt", "r") as f:
    DOMAINS = [x.strip() for x in f.readlines() if x.strip()]


def build_url(stream):
    # якщо вже повний URL
    if stream.startswith("http"):
        return stream

    # інакше генеруємо як у тебе було
    import random

    domain = random.choice(DOMAINS)
    sub = "601"

    return f"https://{sub}.{domain}/{stream}"


with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)


m3u = "#EXTM3U\n"

for cat, items in data.items():
    for item in items:
        title = item["title"]
        streams = item.get("streams", [])

        if not streams:
            continue

        # беремо ПЕРШИЙ або всі
        for s in streams:
            url = build_url(s)

            m3u += f'#EXTINF:-1 group-title="{cat}",{title}\n'
            m3u += url + "\n"

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u)

print("M3U DONE")
