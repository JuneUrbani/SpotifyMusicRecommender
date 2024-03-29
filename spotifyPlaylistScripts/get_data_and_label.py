from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
import json
import spotipy
import time
import sys
import json 
import csv

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

ids = { 'jazz':'spotify:playlist:37i9dQZF1DXbITWG1ZJKYt',
        'rock':'spotify:playlist:37i9dQZF1DWWzBc3TOlaAV',
        'hip-hop':'spotify:playlist:37i9dQZF1DX2RxBh64BHjQ',
        'dance-electronic':'spotify:playlist:37i9dQZF1DXa8NOEUWPn9W',
        'folk':'spotify:playlist:37i9dQZF1DWYV7OOaGhoH0',
        'country':'spotify:playlist:37i9dQZF1DX0bUGQdz5BJG',
        'punk':'spotify:playlist:37i9dQZF1DX9wa6XirBPv8',
        'metal':'spotify:playlist:37i9dQZF1DX5J7FIl4q56G'}

csv_columns = ["name","artists","danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","type","audio_features","id","uri","track_href","analysis_url","duration_ms","time_signature","target"]
csv_file = "data_categorized.csv"
with open(csv_file, 'w+', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

    for genre, pl_id in ids.items():
        offset = 0
        song_urls = []

        while True:
            response = sp.playlist_items(pl_id,
                                         offset=offset,
                                         fields='items.track.id,total',
                                         additional_types=['track'])
            
            if len(response['items']) == 0:
                break
                
            pprint(response['items'])
            offset = offset + len(response['items'])
            print(offset, "/", response['total'])

            for i in range(len(response['items'])):
                song_urls.append(response['items'][i].get("track").get("id"))

        client_credentials_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        sp.trace = True
        
        for i in range(len(song_urls)):
            tids = song_urls[i]

            start = time.time()
            features = sp.audio_features(tids)
            delta = time.time() - start
            
            features[0]['target'] = genre
            features[0]['name'] = sp.track(tids)['name']
            features[0]['artists'] = sp.track(tids)['artists'][0]['name']
            dict_data = features
            for data in dict_data:
                writer.writerow(data)