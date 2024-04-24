import all_time_songs
import artist_songs
import chart as chart

import spotipy
import open_ai
import sqlite3

from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import datetime

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

def return_most_popular_songs(artist_songs_df):
    return artist_songs_df.sort_values('popularity', ascending = False)['name'].reset_index(drop=True)[0]

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

def render_base():
    return render_template('base.html', 
                           top_artist_html = chart.plot_artist_counts(df=all_time_df, top_n = 10),
                           top_songs_html = chart.plot_top_songs_by_popularity(all_time_df, 5))

def render_artist(user_artist, artist_songs_df):    
    return render_template('artist.html', 
                           most_popular_song = return_most_popular_songs(artist_songs_df=artist_songs_df),
                           user_artist = user_artist,
                           chat_gpt_response = open_ai.return_chatgpt_introduction(str(user_artist)),
                           )
def render_album(artist_album_df):
    return render_template('album.html', 
                           album_table = artist_album_df[['AlbumName']].to_html())

def render_customer():
    return render_template('customer.html', 
                           customer_tables = sql_analysis())


@my_app.route('/', methods=['GET','POST']) # NEW
def receive_artist():
    user_artist = "the weeknd"
    if request.method == 'POST':
        user_artist = str(request.form['artist_name'])
    artist_uri = artist_songs.query_artist_uri(user_artist)
    TOP_TRACK_URL = f'https://api.spotify.com/v1/artists/{artist_uri}/top-tracks?market=US'
    album_selection = ['Starboy']
    uri, name, artist_album_df = artist_songs.return_artist_album(sp, user_artist)
    artist_songs_df = artist_songs.return_artist_songs(access_token=ACCESS_TOKEN, top_track_url=TOP_TRACK_URL)
    artist_songs_in_album_df = artist_songs.return_artist_songs_in_album(uri,name,album_names_df=artist_album_df,album_selection=album_selection)
    render_base()
    render_artist(user_artist, artist_songs_df)
    render_album(artist_album_df)
    render_customer()
    

# For use in starting from the terminal 
if __name__ == '__main__':  
   my_app.run()
