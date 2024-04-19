import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def plot_artist_counts(df, top_n=5):
    # Grouping the DataFrame by artist_name and counting the occurrences
    artist_counts = df.groupby('artist_name').size().reset_index(name='count')

    # Sorting the artists by count and selecting the top 20
    top_artists = artist_counts.sort_values(by='count', ascending=False).head(top_n)

    # Creating a bar plot using Plotly Express
    fig = px.bar(top_artists, x='artist_name', y='count', title='Top 10 Artists by Number of Songs all time',
                 labels={'artist_name': 'Artist', 'count': 'Count'})
    return fig.to_html(fig, full_html=False)

def plot_top_songs_by_popularity(df, top_n):
    """
    Plot the top N most popular songs based on the 'popularity' column using Plotly.

    Parameters:
    - df: DataFrame containing song data.
    - top_n: Number of top songs to display.
    
    Returns:
    - plot_html: HTML code of the plot.
    """
    # Extracting the top N most popular songs
    top_popular = df.nlargest(top_n, 'popularity')

    # Creating the bar plot using Plotly
    fig = go.Figure(go.Bar(
        x=top_popular['popularity'],
        y=top_popular['song_name'],
        orientation='h',
        marker=dict(color='skyblue'),
    ))

    fig.update_layout(
        title=f'Top {top_n} Most Popular Songs',
        xaxis_title='Popularity',
        yaxis_title='Song Name',
        yaxis=dict(autorange="reversed"),  # Invert y-axis to have the highest popularity at the top
    )

    plot_html = fig.to_html(full_html=False)
    # fig.show()
    return plot_html