from utils.constants import Constants
from utils.manager import Manager

Constants.init()
Manager.get_token()
Manager.get_spotify_instance()
print(len(Manager.get_songs_ids()))
print(len(Manager.get_songs_features()))
