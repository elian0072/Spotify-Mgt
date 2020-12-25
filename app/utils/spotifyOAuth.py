import requests, base64
from deta import Deta


def getSpotifyAppData(query: str = None):
    """
    Return Dictionary containing the Query as argument.
    If the argument is not recognize, it will be ignored.
    If no query is supplied, all arguments will be supplied
    Possible Args in the Query seperated by an empty space:
    - clientID (Spotify Apps ID)
    - clientSecret (Spotify Apps Secret)
    - redirect (Redirect URL after validation)
    - scopes (Scopes for the Application)
    - state (encoded value for crossChecking)
    - authorization (Spotify Authorization Endpoint)
    - token (Spotify Token Endpoint)
    """
    try:
        r = requests.get("https://poampi.deta.dev/detakey")
        responseJSON = r.json()
        deta = Deta(responseJSON["token"])
        app_DB = deta.Base("applications")
        row = next(app_DB.fetch({"app": "spotify"}))

        CLIENT_ID = row[0]["client_id"]
        CLIENT_SECRET = row[0]["client_secret"]
        REDIRECT = row[0]["redirect_uri"]
        SCOPES = row[0]["scopes"]
        STATE = row[0]["state"]
        AUTH_EP = row[0]["authorize_endpoint"]
        TOKEN_EP = row[0]["token_endpoint"]

        if query is None:
            return {
                "clientID": CLIENT_ID,
                "clientSecret": CLIENT_SECRET,
                "redirect": REDIRECT,
                "scopes": SCOPES,
                "state": STATE,
                "authorization": AUTH_EP,
                "token": TOKEN_EP,
            }

        # Split the Query String using an empty space as separator
        args = query.split(" ")

        DataDir = dict()
        for item in args:
            if item == "clientID":
                DataDir["clientID"] = CLIENT_ID
            elif item == "clientSecret":
                DataDir["clientSecret"] = CLIENT_SECRET
            elif item == "redirect":
                DataDir["redirect"] = REDIRECT
            elif item == "scopes":
                DataDir["scopes"] = SCOPES
            elif item == "state":
                DataDir["state"] = STATE
            elif item == "authorization":
                DataDir["authorization"] = AUTH_EP
            elif item == "tokenURL":
                DataDir["tokenURL"] = TOKEN_EP
            else:
                pass

        return DataDir

    except Exception as e:
        print("An error occured:")
        print(e)


def requestAuthTokenUrl(
    clientID: str, redirectUri: str, scopes: str, state: str, authURL: str
):
    """
    Generate URL for Spotify Authorization
    \n
    - clientID -- Client ID from the Spotify Application
    - redirectUri -- Redirect URI used by the Spotify Application to redirect the use the a specific URL
    - scopes -- Scope used to access the Spotify Application
    - state -- Encoded value for CrossChecking

    """
    RESPONSE_TYPE = "code"
    SHOW_DIALOG = True

    params = {
        "client_id": clientID,
        "response_type": RESPONSE_TYPE,
        "redirect_uri": redirectUri,
        "state": state,
        "scope": scopes,
        "show_dialog": SHOW_DIALOG,
    }
    r = requests.get(authURL, params=params)
    authorizationURL = r.url

    return authorizationURL


def requestSpotifyToken():
    pass


def encodeAuthHeader(clientId: str, clientSecret: str):
    """
    Encode client ID and Client Secret to Base64 (*<base64 encoded client_id:client_secret>*)
    for Authorization Header
    """

    codeString = clientId + ":" + clientSecret
    codeString_bytes = codeString.encode("ascii")
    base64_bytes = base64.b64encode(codeString_bytes)
    authHeaderToString = base64_bytes.decode("ascii")

    return authHeaderToString