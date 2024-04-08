import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import datetime
# from io import StringIO
import requests
import base64 
import os
from dotenv import load_dotenv
# see also python-decouple

load_dotenv()

# accessing and printing value
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

now = datetime.now().date()

client_credentials_manager = SpotifyClientCredentials(
client_id =CLIENT_ID, 
client_secret =CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


# Function to obtain access token
def get_access_token(CLIENT_ID, CLIENT_SECRET):
    # Spotify URL for authentication
    auth_url = 'https://accounts.spotify.com/api/token'
    client_creds = f'{CLIENT_ID}:{CLIENT_SECRET}'
    client_creds_b64 = base64.b64encode(client_creds.encode())
    token_headers = {'Authorization': f'Basic {client_creds_b64.decode()}'}
    token_data = {'grant_type': 'client_credentials'}
    r = requests.post(auth_url, headers=token_headers, data=token_data)
    token_response_data = r.json()
    access_token = token_response_data.get('access_token')
    return access_token

# Function to call Spotify data
def query_Spotify(access_token, url):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    return response.json()

def query_artist_uri(user_artist):
    result = sp.search(user_artist) 
    artist_full_uri = result['tracks']['items'][0]['artists'][0]['uri']
    artist_uri = artist_full_uri.split(":")[2]
    return artist_uri

def return_artist_album(sp, user_artist):
    result = sp.search(user_artist) 
    artist_full_uri = result['tracks']['items'][0]['artists'][0]['uri']
    artist_uri = artist_full_uri.split(":")[2]

    result = sp.search(user_artist) 
    # print(result)
    artist_uri = result['tracks']['items'][0]['artists'][0]['uri']

    sp_albums = sp.artist_albums(artist_uri, album_type='album', country='US')
    name = []
    uri = []
    for i in sp_albums['items']:
        name.append(i['name'])
        uri.append(i['uri'])

    #print(json.dumps(sp_albums['items'][0]['name'], indent=4))
    album_names_df = pd.DataFrame(name)
    album_names_df.columns =['AlbumName']
    album_names_df["URI"] = uri
    return uri,name, album_names_df


def return_artist_songs(access_token, top_track_url):
    # Query Spotify without Spotipy package
    top_tracks_json = query_Spotify(access_token, top_track_url)
    #print(json.dumps(top_tracks_json, indent=4))

    spotify_results_df = pd.DataFrame(top_tracks_json['tracks'])
    spotify_results_df['duration'] = spotify_results_df['duration_ms']/100
    return spotify_results_df[['name','duration_ms','popularity']]

def return_artist_songs_in_album(uri, name, album_names_df, album_selection):
        # remove unmatching albums from album_names_df
    filtered_album_names_df = album_names_df[album_names_df.AlbumName.isin(album_selection) == True].copy()
    # remove uri's from uri that do not exist in filtered data frame
    filtered_uri = [item for item in uri if item in filtered_album_names_df['URI'].values]
    #print(json.dumps(filtered_uri, indent=4))

    # Loop to get song URI for selected albums
    song_name = []
    song_uri = []
    album = []
    count = 0
    for j in filtered_uri:    
        tracks = sp.album_tracks(j, market='US')   
        for i in tracks['items']:
            album.append(name[count])
            song_name.append(i['name'])
            song_uri.append(i['uri'])
        count+=1
    song_name

    acoustic = []; dance = []; energy = []; instrumental = []; liveness = []; loudness = []; speech = []; tempo = []; valence = []

    # Loop throug to get song qualities
    for i in song_uri:
        feat = sp.audio_features(i)[0]
        acoustic.append(feat['acousticness'])
        dance.append(feat['danceability'])
        energy.append(feat['energy'])
        speech.append(feat['speechiness'])
        instrumental.append(feat['instrumentalness'])
        loudness.append(feat['loudness'])
        tempo.append(feat['tempo'])
        liveness.append(feat['liveness'])
        valence.append(feat['valence'])

    #print(json.dumps(song_name, indent=4))
    songs_df = pd.DataFrame({'Name': song_name, 'URI': song_uri, 'acoustic': acoustic,'danceability': dance,
                            'energy': energy,'speechiness': speech,'instrumentalness': instrumental,
                            'loudness': loudness, 'tempo': tempo, 'liveness': liveness,'valence': valence})
    return songs_df

# prompt user input
user_artist = 'The weeknd'
ACCESS_TOKEN = get_access_token(CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET)
artist_uri = query_artist_uri(user_artist)
TOP_TRACK_URL = f'https://api.spotify.com/v1/artists/{artist_uri}/top-tracks?market=US'
album_selection = ['Starboy']

def main():
    uri, name, artist_album_df = return_artist_album(sp, user_artist)
    artist_songs_df = return_artist_songs(access_token=ACCESS_TOKEN, top_track_url=TOP_TRACK_URL)
    artist_songs_in_album_df = return_artist_songs_in_album(uri,name,album_names_df=artist_album_df,album_selection=album_selection)

if __name__ == "__main__":
    main()


        
    