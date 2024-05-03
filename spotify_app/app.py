import all_time_songs
import artist_songs
import chart as chart

import spotipy
import open_ai
import sqlite3

from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import datetime

import giuli
import kaylee

from flask import Flask
from flask import render_template
from flask import request

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


my_app = Flask(__name__)

ACCESS_TOKEN = artist_songs.get_access_token(CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET)

all_time_df, all_time_artist_df, all_time_album_df, all_time_song_df = all_time_songs.return_all_time_songs(sp)

all_time_df = all_time_df.reset_index(drop=True)

def return_artist_songs_appearance_in_all_time(user_artist, all_time_df):
    return all_time_df.loc[all_time_df['artist_name'] == user_artist][['song_name']].to_html()

def sql_analysis():
    sql_get_all_customers_and_stays = """
    SELECT * FROM customers
    """

    con = sqlite3.connect("customervisit.db") # establish connection to database (point to the right database)
    cur = con.cursor() # open 'access' to the database
    cur.execute(sql_get_all_customers_and_stays)
    result = cur.fetchall()
    con.close()
    table = pd.DataFrame(result, columns=['customer_id', 'name', 'age'])  
    return table.to_html(index=False, classes='table table-striped')


@my_app.route('/', methods=['GET','POST']) # NEW
def render_index():
    user_artist = "the weeknd"
    album_selection = ['Starboy']
    if request.method == 'POST':
        user_artist = str(request.form['artist_name'])
    artist_uri = artist_songs.query_artist_uri(user_artist)
    TOP_TRACK_URL = f'https://api.spotify.com/v1/artists/{artist_uri}/top-tracks?market=US'
    uri, name, artist_album_df = artist_songs.return_artist_album(sp, user_artist)
    artist_songs_df = artist_songs.return_artist_songs(access_token=ACCESS_TOKEN, top_track_url=TOP_TRACK_URL)
    return render_template('index.html', 
                           user_artist = user_artist,
                           most_popular_song = kaylee.return_most_popular_songs(artist_songs_df=artist_songs_df),
                           least_popular_song = kaylee.return_least_popular_songs(artist_songs_df=artist_songs_df),

                           apperance_response = giuli.return_artist_appearance_in_all_time(user_artist=user_artist, all_time_df=all_time_df),
                           songs_in_all_time_table = return_artist_songs_appearance_in_all_time(user_artist=user_artist, all_time_df=all_time_df),
        
                           chat_gpt_response = open_ai.return_chatgpt_introduction(str(user_artist)),

                           top_artist_html = chart.plot_artist_counts(df=all_time_df, top_n = 10),
                           top_songs_html = chart.plot_top_songs_by_popularity(all_time_df, 5),

                           album_table = artist_album_df[['AlbumName']].to_html(),
                           customer_tables = sql_analysis()
                           )

# For use in starting from the terminal 
if __name__ == '__main__':  
   my_app.run()
