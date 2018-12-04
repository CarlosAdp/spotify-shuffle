from utils.constants import Constants
from spotipy.util import prompt_for_user_token
import spotipy
import random

class Manager:
    @classmethod
    def init(cls) -> None:
        return

    @classmethod
    def get_token(cls) -> str:
        Constants.token = prompt_for_user_token(username=Constants.username,
                scope=Constants.scopes,
                client_id=Constants.client_id,
                client_secret=Constants.client_secret,
                redirect_uri=Constants.redirect_uri)

        print(Constants.token)
        return Constants.token

    @classmethod
    def get_spotify_instance(cls) -> None:
        cls.spotify_instance = spotipy.Spotify(auth = Constants.token)
        return cls.spotify_instance

    @classmethod
    def get_songs_ids(cls) -> list:
        result = []

        partial_result = cls.spotify_instance.current_user_saved_tracks(limit = 50)
        result = result + [item['track']['id'] for item in partial_result['items']]

        while(partial_result['next']):
            partial_result = cls.spotify_instance.next(partial_result)
            result = result + [item['track']['id'] for item in partial_result['items']]

        cls.songs_ids = result
        return result

    @classmethod
    def get_songs_features(cls) -> None:
        songs_ids_split_50 = [cls.songs_ids[i : i + 50] for i in range(0, len(cls.songs_ids), 50)]

        cls.songs_features_denormalized = []
        for songs_ids in songs_ids_split_50:
            cls.songs_features_denormalized += cls.spotify_instance.audio_features(
                    tracks = songs_ids)

        return cls.songs_features_denormalized

    @classmethod
    def pick_first_song_id(cls) -> str:
        cls.first_song_id = random.choice(cls.songs_ids)
        return cls.first_song_id
