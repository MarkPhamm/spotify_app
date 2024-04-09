import all_time_songs
import artist_songs
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import datetime


from flask import Flask
from flask import render_template


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

# prompt user input
user_artist = 'The weeknd'
ACCESS_TOKEN = artist_songs.get_access_token(CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET)
artist_uri = artist_songs.query_artist_uri(user_artist)
TOP_TRACK_URL = f'https://api.spotify.com/v1/artists/{artist_uri}/top-tracks?market=US'
album_selection = ['Starboy']

all_time_df, all_time_artist_df, all_time_album_df, all_time_song_df = all_time_songs.return_all_time_songs(sp)

uri, name, artist_album_df = artist_songs.return_artist_album(sp, user_artist)
artist_songs_df = artist_songs.return_artist_songs(access_token=ACCESS_TOKEN, top_track_url=TOP_TRACK_URL)
artist_songs_in_album_df = artist_songs.return_artist_songs_in_album(uri,name,album_names_df=artist_album_df,album_selection=album_selection)

# print(artist_songs_in_album_df.head())
# print(artist_songs_df)
# print(artist_album_df)

# all_time_df.to_csv(r"spotify_app\static\data\all_time_df.csv")
# all_time_artist_df.to_csv(r"spotify_app\static\data\all_time_artist_df.csv")
# all_time_album_df.to_csv(r"spotify_app\static\data\all_time_album_df.csv")
# all_time_song_df.to_csv(r"spotify_app\static\data\all_time_song_df.csv")

# artist_album_df.to_csv(r"spotify_app\static\data\artist_album_df.csv")
# artist_songs_df.to_csv(r"spotify_app\static\data\artist_songs_df.csv")
# artist_songs_in_album_df.to_csv(r"spotify_app\static\data\artist_songs_in_album_df.csv")

my_app = Flask(__name__)
@my_app.route('/')
def index():
    return render_template('index.html', most_popular_song = artist_songs_df.sort_values('popularity', ascending = False)['name'].head(1))

# For use in starting from the terminal 
if __name__ == '__main__':  
   my_app.run()
