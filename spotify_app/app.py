import all_time_songs
import artist_songs
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import datetime

CLIENT_ID = "3bb988d3549f41908d0a7ab799d962e5"
CLIENT_SECRET = "7a9146e9861249ebba524a14d9f3a614"

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

print(artist_songs_in_album_df.head())