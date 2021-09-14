import requests
import json
import re
import codecs

class DataLoader():
    def __init__(self, n=1):
        create_isrc_files(n)
        return

# 各ジャンルにつきn*100曲のISRCコードをファイルに書き出します
def create_isrc_files(n):
    
    r = requests.get("https://www.beatport.com/api/v4/catalog/genres")
    lists = r.json()["results"]
    
    for i, genre in enumerate(lists[23:]):
        print("loading " + genre["name"] + f"...[{i+1}/{len(lists)}]")
        track_ids = []
        isrc = []
        slug = genre["slug"]
        id = genre["id"]
        path = f"./isrc/{slug}.txt"
        for batch in range(n):
            uri = f"https://www.beatport.com/genre/{slug}/{id}/tracks?page={batch+1}"
            r = requests.get(uri)
            track_ids.extend(re.findall(r'data-track="([0-9]+)', r.text))
        print("loaded ids")
        print("loading ISRC...")
        for j, track_id in enumerate(track_ids):
            print(f"[{j+1}/{len(track_ids)}]")
            uri = f"https://www.beatport.com/api/v4/catalog/tracks/{track_id}"
            r = requests.get(uri)
            try:
                isrc.append(r.json()["isrc"])
            except:
                print('no isrc')
        print(isrc, file=codecs.open(path, 'w', 'utf-8'))
