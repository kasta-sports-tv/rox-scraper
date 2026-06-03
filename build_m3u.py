import json

with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

lines = ["#EXTM3U"]

count = 0

for cat, items in data.items():
    for item in items:
        if not item.get("stream"):
            continue

        lines.append(f'#EXTINF:-1 group-title="{cat.upper()}",{item["title"]}')
        lines.append(item["stream"])
        count += 1

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("TOTAL:", count)
