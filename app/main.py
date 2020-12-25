from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from utils.spotifyOAuth import encodeAuthHeader, getSpotifyAppData, requestAuthTokenUrl

app = FastAPI(title="Spotify Web API", description="Access Spotify Web Service")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def getMainPage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/spotifyAuth")
async def spotifyProcess():
    """
    Genrerates the requiered HTTP call to the Spotify Service in order
    to give the user the opportunity to give access to its Spotify account
    for the application
    """
    data = getSpotifyAppData("clientID redirect scopes state authorization")
    url = requestAuthTokenUrl(
        data["clientID"],
        data["redirect"],
        data["scopes"],
        data["state"],
        data["authorization"],
    )
    return RedirectResponse(url, status_code=302)


@app.get("/callback")
async def callback_uri(
    request: Request,
    response: Response,
    code: str = None,
    error: str = None,
    state: str = None,
):
    """
    Handles Spotify redirection with the generated code if the user
    allowed the App to access its account
    """
    callback = dict()

    if code:
        callback["code"] = code
        response.status_code = status.HTTP_200_OK
    if error:
        callback["error"] = error
        response.status_code = status.HTTP_403_FORBIDDEN
    if state:
        callback["state"] = state

    # Variabalize dictionary for Jinja HTML Response
    return templates.TemplateResponse(
        "SpotifyService.html",
        {
            "request": request,
            "status_code": response.status_code,
            "code": code,
            "state": state,
        },
    )
