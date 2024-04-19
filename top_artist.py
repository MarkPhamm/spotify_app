import pandas as pd
import plotly.express as px

def plot_artist_counts(df, top_n=5):
    # Grouping the DataFrame by artist_name and counting the occurrences
    artist_counts = df.groupby('artist_name').size().reset_index(name='count')

    # Sorting the artists by count and selecting the top 20
    top_artists = artist_counts.sort_values(by='count', ascending=False).head(top_n)

    # Creating a bar plot using Plotly Express
    fig = px.bar(top_artists, x='artist_name', y='count', title='Top 20 Artists by Number of Songs all time',
                 labels={'artist_name': 'Artist', 'count': 'Count'})
    return fig.to_html(fig, full_html=False)

