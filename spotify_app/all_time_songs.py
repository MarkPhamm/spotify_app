import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import datetime
from io import StringIO
import requests
import base64 
import os
from dotenv import load_dotenv
# see also python-decouple

load_dotenv()

# accessing and printing value
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(
client_id =CLIENT_ID, 
client_secret =CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

now = datetime.now().date()

def return_all_time_songs(sp):
    playlist_link = 'https://open.spotify.com/playlist/2YRe7HRKNRvXdJBp9nXFza'

    playlist_URI = playlist_link.split("/")[-1].split('?')[0]
    sp.playlist_tracks(playlist_URI)

    # Initialize an empty list to store all the tracks
    all_tracks = []

    # Initialize the offset to 0
    offset = 0

    # Set the limit to the maximum allowed (100 tracks per request)
    limit = 100

    while True:
        # Retrieve the next batch of tracks
        batch = sp.playlist_tracks(playlist_URI, offset=offset, limit=limit)

        # Add the batch of tracks to the list
        all_tracks.extend(batch['items'])

        # Check if there are more tracks to retrieve
        if len(batch['items']) < limit:
            break

        # Increment the offset for the next request
        offset += limit

    # Continue with the rest of your code to process the data

    # The code that follows can remain the same as in your original code
    data = {
        'href': batch['href'],  # The last href from the loop
        'items': all_tracks
    }

    album_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['album']['external_urls']['spotify']
        album_element = {'album_id':album_id, 'name':album_name, 'release_date' :album_release_date, 'total_tracks':album_total_tracks, 'url':album_url}
        album_list.append(album_element)

    album_df = pd.DataFrame.from_dict(album_list)
    # album_df = album_df.drop_duplicates(subset=['album_id'])
    album_df['release_date'] = pd.to_datetime(album_df['release_date'],format='mixed')
    album_df['album_old'] = now - album_df['release_date'].dt.date
    album_df['album_old'] = album_df['album_old'].apply(lambda x: x.days)
    album_df = album_df.rename(columns={'name': 'album_name'})
    album_df['album_name'] = album_df['album_name'].str.replace(',', ';')

    artist_list = []
    for row in data['items']:
        for key, value in row.items():
            if key == 'track':
                for artist in value['artists']:
                    artist_dict = {'artist_id': artist['id'], 'artist_name':artist['name'], 'external_url': artist['href']}
                    artist_list.append(artist_dict)

    artist_df = pd.DataFrame.from_dict(artist_list)
    artist_df = artist_df.drop_duplicates(subset=['artist_id'])
    artist_df['artist_name'] = artist_df['artist_name'].str.replace(',', ';')

    song_list = []
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration =  row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        song_element = {'song_id': song_id, 'song_name': song_name, 'duration_ms': song_duration, 'url': song_url, 
                    'popularity': song_popularity, 'song_added': song_added, 'album_id': album_id,
                    'artist_id':artist_id
                    }
        song_list.append(song_element)
    
    song_df = pd.DataFrame.from_dict(song_list)
    song_df['song_release'] = pd.to_datetime(song_df['song_added'], format='mixed')
    song_df['song_old'] = now - song_df['song_release'].dt.date
    song_df['song_old'] = song_df['song_old'].apply(lambda x: x.days)
    song_df['song_name'] = song_df['song_name'].str.replace(',', ';')

    df = song_df.merge(album_df, how="inner", on="album_id")
    df = df.merge(artist_df, how="inner", on="artist_id")
    df.drop_duplicates(inplace=True)
    df.drop(columns=['song_id','artist_id','album_id','total_tracks','url_y','external_url'], inplace = True)
    return df,artist_df,album_df,song_df

def main():
    all_time_df, all_time_artist_df,all_time_album_df,all_time_song_df = return_all_time_songs(sp)

if __name__ == "__main__":
    main()