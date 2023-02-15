import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='26b948d574774a0697ca4f33cb8cca12',
                                               client_secret='0a298958a0d243db85d6d330fe86d4da',
                                               redirect_uri='https://www.google.com/',
                                               scope='user-library-read'))

track_name = input("Enter the name of the song you want to play: ")

# search for the track
results = sp.search(q=track_name, type="track")

# get the URI of the first track in the search results
track_uri = results["tracks"]["items"][0]["uri"]

# start playback of the track
sp.start_playback(uris=[track_uri])