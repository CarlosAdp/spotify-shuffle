import spotipy
from utils.manager import Manager
from utils.constants import Constants

Constants.init()
Manager.init()
Manager.get_token()
sp = Manager.get_spotify_instance()
songs_ids = Manager.get_songs_ids()

limit = 50
[sp.current_user_saved_tracks_delete(tracks = songs_ids[i:i + limit]) for i in range(0, len(songs_ids), limit)]
