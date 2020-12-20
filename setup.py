import requests, json
from deta import Deta

r = requests.get('https://poampi.deta.dev/detakey')
responseJSON = r.json()
deta = Deta(responseJSON["token"])
spotify_db = deta.Base("spotify")

try:
        key = next(spotify_db.fetch())
        if not key:
                spotify_db.put({
                "SPOTIPY_CLIENT_ID":"361fb418636a4e4e830f96a5d5d6b533",
                "SPOTIPY_CLIENT_SECRET" :"922e4d319ff74d4b81f7e03096ff2c86",
                "SPOTIPY_REDIRECT_URI":"http://localhost"
        })
except Exception as e:
        print(e)
