from utils.manager import Manager
from utils.library import LocalLibrary
from utils.spotify_utils import SpotifyUtils

if __name__ == "__main__":
    Manager.init()
    SpotifyUtils.authenticate()
    LocalLibrary.update()
    LocalLibrary.save()
