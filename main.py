import os
import spotipy
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

date = input(
    "Which year to you want to travel to ? Type the date in this format YYYY-MM-DD: "
)

URL = "https://www.billboard.com/charts/hot-100/"
year = date.split("-")[0]
song_uris = []

response = requests.get(url=f"{URL}{date}")
web_side_html = response.text

soup = BeautifulSoup(web_side_html, "html.parser")
song_names_h3 = soup.findAll("h3", id="title-of-a-story", class_="a-no-trucate")
song_names = [song.getText().strip() for song in song_names_h3]

artist_name_span = soup.select("span.c-label.a-no-trucate")
artist_names = [artist.getText().strip() for artist in artist_name_span]


# Spotify API
client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-read-private user-read-email playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
    )
)

user_id = sp.current_user()["id"]

for song, artist in zip(song_names, artist_names):
    result = sp.search(q=f"track:{song} artist:{artist}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} - {artist} doesn't exist in Spotify. Skipped.")

pprint(len(song_uris))

# Play list creation
play_list_id = sp.user_playlist_create( user=user_id, name=f"{date} Billboard 100", public=False).get("id")
sp.playlist_add_items(playlist_id=play_list_id, items=song_uris)

