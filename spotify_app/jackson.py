import pandas as pd

def return_albums_in_all_time_list(artist_album_df, all_time_album_df):
    merge = pd.merge(artist_album_df, all_time_album_df, how='inner', left_on = 'AlbumName', right_on = 'album_name')
    merge = merge.drop_duplicates(subset=['AlbumName'])
    return merge[['album_id', 'album_name', 'release_date','total_tracks', 'url','album_old']].to_html()

def return_number_of_album_in_all_time_list(artist_album_df, all_time_album_df):
    merge = pd.merge(artist_album_df, all_time_album_df, how='inner', left_on = 'AlbumName', right_on = 'album_name')
    merge = merge.drop_duplicates(subset=['AlbumName'])
    return len(merge)