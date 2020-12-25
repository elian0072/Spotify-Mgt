import requests, json
from deta import Deta

r = requests.get('https://poampi.deta.dev/detakey')
responseJSON = r.json()
deta = Deta(responseJSON["token"])
deta_DB = deta.Base("applications")

try:
        key = next(deta_DB.fetch())
        if not key:
                deta_DB.put({
                "client_id" : "361fb418636a4e4e830f96a5d5d6b533",
                "client_secret" : "922e4d319ff74d4b81f7e03096ff2c86",
                "redirect_uri" : "http://localhost:8000/callback",
                "app":"spotify",
                "scopes" : "user-read-playback-state",
                "state" : "SpotifyWebAPI",
                "authorize_endpoint" : "https://accounts.spotify.com/authorize",
                "token_endpoint" : "https://accounts.spotify.com/api/token"
                })
                print("Added row to Database")
except Exception as e:
        print(e)
