import requests
import json
import re
import codecs
import numpy as np
import time
from . import credentials
import base64

global headers

class DataLoader():
    def __init__(self, add_new=False, start=0, end=0):
        if add_new == True:
            if start == 0 or start > end:
                print("Check out of start and end number.")
                exit()
            else:
                add_new_data(start, end)
        (self.data, self.target) = load_data()
        return

# 新しく各ジャンルのstartページ目からendページ目までの曲データをファイルに保存
def add_new_data(start, end):
    create_isrc_files(start, end)
    download_features()

# ファイルから教師データをロードします
def load_data():
    data = []
    target = []
    for i, genre in enumerate(genres_list):
        data_genre = np.loadtxt(f"./data/{genre}.txt", delimiter='\n', dtype='str')
        for d in data_genre:
            d = d.replace("[", "").replace("]", "")
            data.append(np.fromstring(d, dtype=float, sep=', ').tolist())
            target.append(i)
    return (np.array(data), np.array(target))

# 各ジャンルにつきn*100曲のISRCコードをファイルに書き出す
def create_isrc_files(start, end):
    r = requests.get("https://www.beatport.com/api/v4/catalog/genres")
    lists = r.json()["results"]
    
    for i, genre in enumerate(lists):
        print("loading " + genre["name"] + f"...[{i+1}/{len(lists)}]")
        track_ids = []
        isrc = []
        slug = genre["slug"]
        id = genre["id"]
        path = f"./isrc/{slug}.txt"
        for batch in range(start, end):
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
        
# ジャンルごとの教師データをテキストファイルに保存
def download_features():
    for i, genre in enumerate(genres_list[27:]):
        set_token_to_headers()
        data = []
        ids = get_spotify_ids_of(genre)
        print(f"Downloading features of {genre}...[{len(ids)}]")
        for id in ids:
            d = get_spotify_features(id)
            if d is not None:
                data.append(d)
            print(d)
            print(d, file=codecs.open(f"./data/{genre}.txt", 'a', 'utf-8'))

# あるジャンルについてspotifyのIDの集合を作成
def get_spotify_ids_of(genre):
    spotify_ids = []
    isrc = np.loadtxt(f"./isrc/{genre}.txt", delimiter=', ', dtype='str')
    print(f"Getting spotify IDs of {genre}...")
    for i in isrc:
        id = get_spotify_id(i.replace("[", "").replace("]", "").replace("\'", ""))
        print(id)
        if id is not None:
            spotify_ids.append(id)
    return spotify_ids

# isrcコードからspotifyのIDを取得
def get_spotify_id(isrc):
    payload = {'q': f'isrc:{isrc}', 'type': 'track'}
    global headers
    r = requests.get("https://api.spotify.com/v1/search", params=payload, headers=headers)
    time.sleep(0.5)
    try:
        items = r.json()["tracks"]["items"]
        if len(items) >= 1:
            return items[0]["id"]
    except:
        print(r.json)

def get_spotify_features(id):
    # get item
    global headers
    r = requests.get(f"https://api.spotify.com/v1/audio-features/{id}", headers=headers)
    time.sleep(0.5)
    item = r.json()
    
    data = []
    try:
        data.append(item["danceability"])
    except:
        print("not found")
        return
    data.append(item["energy"])
    data.append(item["key"])
    data.append(item["loudness"])
    data.append(item["mode"])
    data.append(item["speechiness"])
    data.append(item["acousticness"])
    data.append(item["instrumentalness"])
    data.append(item["liveness"])
    data.append(item["valence"])
    data.append(item["tempo"])
    data.append(item["duration_ms"])
    data.append(item["time_signature"])
    return data

def get_spotify_token():
    # credentials
    client_id = credentials.credentials["client_id"]
    client_secret = credentials.credentials["client_secret"]
    
    # get token
    token_uri = 'https://accounts.spotify.com/api/token'
    authorization = 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()
    headers = {'Authorization': authorization}
    payload = {'grant_type': 'client_credentials'}
    access_token = requests.post(token_uri, data=payload, headers=headers).json()['access_token']
    
    return access_token

def set_token_to_headers():
    token = get_spotify_token()
    global headers
    headers = {'Authorization': f'Bearer {token}'}

genres_list = [
    "140-deep-dubstep-grime",
    "afro-house",
    "bass-club",
    "bass-house",
    "breaks-breakbeat-uk-bass",      
    "dance-electro-pop",
    "deep-house",
    "dj-tools",
    "drum-bass",
    "dubstep",
    "electro-classic-detroit-modern",
    "electronica",
    "funky-house",
    "hard-dance-hardcore",
    "hard-techno",
    "house",
    "indie-dance",
    "jackin-house",
    "mainstage",
    "melodic-house-techno",
    "minimal-deep-tech",
    "nu-disco-disco",
    "organic-house-downtempo",       
    "progressive-house",
    "psy-trance",
    "tech-house",
    "techno-peak-time-driving",      
    "techno-raw-deep-hypnotic",      
    "trance",
    "trap-wave",
    "uk-garage-bassline"
]