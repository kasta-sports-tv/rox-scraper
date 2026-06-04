import json

with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

m3u = "#EXTM3U\n"

for cat, items in data.items():

    # soccer показуємо як football
    group_name = "football" if cat == "soccer" else cat

    for item in items:
        title = item.get("title", "Unknown")
        streams = item.get("streams", [])

        if not streams:
            continue

        # беремо тільки перший робочий
        stream = streams[0]

        m3u += f'#EXTINF:-1 group-title="{group_name}",{title}\n'
        m3u += stream + "\n"

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u)

print("M3U DONE")
