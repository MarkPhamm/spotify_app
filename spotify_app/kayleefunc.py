def sort_songs(df):
    df.drop(columns = 'Unnamed: 0')
    rec_list = []
    for i in ['acoustic', 'danceability', 'energy', 'speechiness', 'instrumentalness', 'loudness', 'tempo', 'liveness','valence']:
        rec_song = df.sort_values(i, ascending=False)['Name'].head(1).to_string()
        print(f"The best songs base on {i} is {rec_song}")
        rec_list.append({i:rec_song}) 
    return rec_list