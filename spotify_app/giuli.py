def return_artist_appearance_in_all_time(user_artist, all_time_df):
    number_of_appearance = len(all_time_df.loc[all_time_df['artist_name'] == user_artist])
    if number_of_appearance == 0:
        return("Unique Choice, your artist has never appeared on the all-time list.")
    return(F"Wow, your artist has {number_of_appearance} songs on the all time list.")