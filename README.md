# Spotify Song Recommendation Webpage

This Flask-based web application provides song recommendations based on user preferences using the Spotify API.

## Features

- User-friendly interface to input artist and output song recommendations based on artist information.
- Utilizes the Spotify API to fetch song data and provide tailored recommendations.
- Responsive design with HTML and CSS for seamless user experience.

## Prerequisites

- Python 3.x installed on your system.
- Flask library installed (`pip install Flask`).
- [Spotify Developer Account](https://developer.spotify.com/) to access the Spotify API.

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/MarkPhamm/spotify_app
    ```

2. Navigate to the project directory:

    ```bash
    cd spotify_app
    ```

3. Create a `.env` file in the project directory and add your Spotify API credentials:

    ```
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    ```

   Replace `your_client_id` and `your_client_secret` with your actual Spotify API credentials obtained from your Spotify Developer Account.

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the Flask server:

    ```bash
    python app.py
    ```