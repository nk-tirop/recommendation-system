import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.neighbors import NearestNeighbors
import pandas as pd

# Connect to the Spotify API using Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='26b948d574774a0697ca4f33cb8cca12',
                                               client_secret='0a298958a0d243db85d6d330fe86d4da',
                                               redirect_uri='https://www.google.com/',
                                               scope='user-library-read'))

# Retrieve a list of your liked songs from your Spotify account using Spotipy
results = sp.current_user_saved_tracks(limit=50)

# Extract features of each liked song, such as artist, genre, and tempo
song_features = []
liked_songs = []
for item in results['items']:
    track = item['track']
    features = sp.audio_features(track['id'])[0]
    song_feature = {'artist': track['artists'][0]['name'],
                    'name': track['name'],
                    'acousticness': features['acousticness'],
                    'danceability': features['danceability'],
                    'energy': features['energy'],
                    'instrumentalness': features['instrumentalness'],
                    'key': features['key'],
                    'liveness': features['liveness'],
                    'loudness': features['loudness'],
                    'speechiness': features['speechiness'],
                    'tempo': features['tempo'],
                    'valence': features['valence']}
    song_features.append(song_feature)
    liked_songs.append(track['id'])

# Use a machine learning algorithm (k-nearest neighbors) to create a recommendation model based on the features of your liked songs
X = pd.DataFrame(song_features)
X = X.drop(['artist', 'name'], axis=1)
nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(X)

# Use the recommendation model to generate a list of recommended songs for you to listen to
song_idx = nn.kneighbors(X.iloc[0].values.reshape(1,-1), n_neighbors=11)[1][0]
recommendations = []
for i in song_idx:
    if len(recommendations) == 10:
        break
    song_id = results['items'][i]['track']['id']
    if song_id not in liked_songs:
        recommendations.append({'artist': results['items'][i]['track']['artists'][0]['name'], 
                                'name': results['items'][i]['track']['name']})

# Print the recommended songs
print("Recommended songs:")
for song in recommendations:
    print(f"{song['artist']} - {song['name']}")
