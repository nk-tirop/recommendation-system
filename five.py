import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import os

# Connect to the Spotify API using Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='26b948d574774a0697ca4f33cb8cca12',
                                               client_secret='0a298958a0d243db85d6d330fe86d4da',
                                               redirect_uri='https://www.google.com/',
                                               scope='user-library-read'))
from collections import defaultdict

def find_song(name, artist_name):
  
    """
    This function returns a dataframe with data for a song given the name and artist name.
    The function uses Spotipy to fetch audio features and metadata for the specified song.
    
    """
    
    song_data = defaultdict()
    results = sp.search(q='track: {} artist: {}'.format(name, artist_name), limit=1)
    if results['tracks']['items'] == []:
        return None
    
    results = results['tracks']['items'][0]

    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]
    
    song_data['name'] = [name]
    song_data['artist_name'] = [artist_name]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]
    
    for key, value in audio_features.items():
        song_data[key] = value
    
    return pd.DataFrame(song_data)
spotify_data = pd.read_csv('data/processed_data.csv')
# Find audio features for each song
audio_features = spotify_data[['name', 'artist_name']].apply(lambda x: find_song(x['name'], x['artist_name']), axis=1)

# Merge audio features with processed data
spotify_data_with_audio_features = pd.concat([spotify_data, audio_features], axis=1)

# Save data to CSV file
spotify_data_with_audio_features.to_csv('data/processed_data_with_audio_features.csv', index=False)


print(find_song('red','taylor swift'))
