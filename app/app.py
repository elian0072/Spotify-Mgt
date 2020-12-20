import spotipy, requests, json
from spotipy.oauth2 import SpotifyOAuth
from deta import Deta

r = requests.get('https://poampi.deta.dev/detakey')
responseJSON = r.json()
deta = Deta(responseJSON["token"])
spotify_db = deta.Base("spotify")

row = next(spotify_db.fetch())

CLIENT_ID = row[0]["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = row[0]["SPOTIPY_CLIENT_SECRET"]
REDIRECT = row[0]["SPOTIPY_REDIRECT_URI"]

scope = "user-read-playback-state user-read-private user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                            client_id=CLIENT_ID, 
                                            client_secret=CLIENT_SECRET, 
                                            redirect_uri=REDIRECT))

# result = spotify.search('Skrillex', limit=1, type='artist')

devices = sp.current_user()

print(json.dumps(devices, indent=4, sort_keys=True))