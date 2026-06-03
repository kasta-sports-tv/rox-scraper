import json

with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

m3u = "#EXTM3U\n"

for cat, items in data.items():
    for item in items:
        title = item.get("title", "No title")
        streams = item.get("streams", [])

        for s in streams:
            m3u += f'#EXTINF:-1 group-title="{cat}",{title}\n'
            m3u += s + "\n"

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u)

print("M3U DONE")
