import json
import os

if not os.path.exists("output.json"):
    print("ERROR: output.json not found")
    exit(1)

with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

m3u = "#EXTM3U\n"

for cat, items in data.items():
    if not isinstance(items, list):
        continue

    for item in items:
        title = item.get("title", "No title")
        streams = item.get("streams") or []

        if not isinstance(streams, list):
            continue

        for s in streams:
            if not s:
                continue

            m3u += f'#EXTINF:-1 group-title="{cat}",{title}\n'
            m3u += s + "\n"

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u)

print("M3U DONE")
