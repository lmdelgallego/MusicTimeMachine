import os
import spotipy
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# date = input(
#     "Which year to you want to travel to ? Type the date in this format YYYY-MM-DD: "
# )

# URL = "https://www.billboard.com/charts/hot-100/"

# response = requests.get(url=f"{URL}{date}")
# web_side_html = response.text

# soup = BeautifulSoup(web_side_html, "html.parser")
# song_names_h3 = soup.findAll("h3", id="title-of-a-story", class_="a-no-trucate")
# song_names = [song.getText().strip() for song in song_names_h3]

# pprint(song_names)
# pprint(len(song_names))


# Spotify API
client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
    )
)

user_id = sp.current_user()["id"]
print(user_id)
# results = sp.search(q="weezer", limit=20)
# for idx, track in enumerate(results["tracks"]["items"]):
#     print(idx, track["name"])
