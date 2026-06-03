import json

with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

lines = ["#EXTM3U"]

total = 0

for cat, items in data.items():
    for item in items:

        streams = item.get("streams", [])

        if not streams:
            continue

        title = item.get("title", "Unknown")

        # 🔥 додаємо ВСІ стріми одного матчу
        for s in streams:
            lines.append(f'#EXTINF:-1 group-title="{cat.upper()}",{title}')
            lines.append(s)
            total += 1

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("TOTAL STREAMS:", total)
print("M3U DONE")
