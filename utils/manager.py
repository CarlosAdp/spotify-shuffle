from utils.constants import Constants
from spotipy.util import prompt_for_user_token
import spotipy
import random

class Manager:
    @classmethod
    def init(cls) -> None:
        cls.features_weights = [5, 5, 1, 5, 5, 2, 5, 5, 5, 4, 2, 5]
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
    def get_spotify_instance(cls) -> spotipy.client.Spotify:
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
    def pick_base_song_id(cls) -> str:
        cls.base_song_id = random.choice(cls.songs_ids)
        cls.base_song_denormalized_features = cls.spotify_instance.audio_features(tracks = [cls.base_song_id])[0]
        cls.base_song_normalized_features = cls.normalize_features(cls.base_song_denormalized_features)
        return cls.base_song_id

    @classmethod
    def get_candidates_ids(cls) -> list:
        random.shuffle(cls.songs_ids)
        cls.songs_ids = cls.songs_ids[:1000]

    @classmethod
    def get_songs_features(cls) -> None:
        songs_ids_split_50 = [cls.songs_ids[i : i + 50] for i in range(0, len(cls.songs_ids), 50)]

        cls.songs_features_denormalized = []
        for songs_ids in songs_ids_split_50:
            cls.songs_features_denormalized += cls.spotify_instance.audio_features(
                    tracks = songs_ids)

        cls.songs_features_normalized = []
        for features in cls.songs_features_denormalized:
            cls.songs_features_normalized.append(cls.normalize_features(features))

    @classmethod
    def get_similar_songs(cls) -> list:
        return [cls.base_song_id, 
                list(zip(*sorted(cls.songs_features_normalized, key = lambda item : cls.distance_to_base_song(item))[:49]))[0]]

    @classmethod
    def normalize_features(cls, denormalized_features) -> None:
        song_id = denormalized_features['id']
        normalized_features = [
                denormalized_features['acousticness'],
                denormalized_features['danceability'],
                float(denormalized_features['duration_ms'])/3600000,
                denormalized_features['energy'],
                denormalized_features['instrumentalness'],
                max(float(2 * denormalized_features['key'] + denormalized_features['mode'])/23, 0),
                denormalized_features['liveness'],
                float(denormalized_features['loudness'] + 60)/60,
                denormalized_features['speechiness'],
                min(float(denormalized_features['tempo'])/500, 1),
                float(denormalized_features['time_signature'] - 2)/18,
                denormalized_features['valence']
                ]
        return song_id, normalized_features

    @classmethod
    def distance_to_base_song(cls, target_song) -> float:
        p1 = cls.base_song_normalized_features[1]
        p2 = target_song[1]
        diff = [w * (i1 - i2) * (i1 - i2) for w, i1, i2 in zip(cls.features_weights, p1, p2)] 
        return sum(diff)
