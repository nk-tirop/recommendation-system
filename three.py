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

# Retrieve a list of Hot Hits Kenya's top tracks
hot_hits_kenya_playlist_id = '37i9dQZF1DWWWXigQZAD8B' # Hot Hits Kenya playlist ID
hot_hits_kenya_tracks = sp.playlist_tracks(hot_hits_kenya_playlist_id, limit=50)

# Extract features of each Hot Hits Kenya top track
hot_hits_kenya_features = []
for item in hot_hits_kenya_tracks['items']:
    track = item['track']
    features = sp.audio_features(track['id'])[0]
    hot_hits_kenya_feature = {'artist': track['artists'][0]['name'],
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
    hot_hits_kenya_features.append(hot_hits_kenya_feature)

# Combine your liked songs and Hot Hits Kenya top tracks into a single dataframe
df = pd.concat([pd.DataFrame(song_features), pd.DataFrame(hot_hits_kenya_features)])

# Use a machine learning algorithm (k-nearest neighbors) to create a recommendation model based on the features of your liked songs and Hot Hits Kenya top tracks
X = df.drop(['artist', 'name'], axis=1)
nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(X)

# Use the recommendation model to generate a list of recommended songs for you to listen to
song_idx = nn.kneighbors(X.iloc[0].values.reshape(1,-1), n_neighbors=10)[1][0]
print('\nThe following songs are recommended for you to listen to: \n')
print(df.iloc[song_idx]['name'])