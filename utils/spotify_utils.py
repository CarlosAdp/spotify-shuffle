import spotipy
from utils.constants import Constants
from spotipy.util import prompt_for_user_token

class SpotifyUtils:
    """
    Classe que abstrai procedimentos relacionados ao Spotify
    """
    _spotify_connection = spotipy.client.Spotify
    @classmethod
    def authenticate(cls) -> None:
        cls._token = prompt_for_user_token(username=Constants.spotify_username,
                scope=Constants.spotify_scopes,
                client_id=Constants.spotify_client_id,
                client_secret=Constants.spotify_client_secret,
                redirect_uri=Constants.spotify_redirect_uri)
        cls._spotify_connection = spotipy.Spotify(auth=cls._token)

    @classmethod
    def get_user_tracks(cls) -> list:
        tracks_infos = cls._execute_spotify_command(spotipy.client.Spotify.current_user_saved_tracks, (Constants.spotify_limit, ))
        return [item['track'] for item in tracks_infos]

    @classmethod
    def get_tracks_features(cls, tracks_ids : list) -> list:
        result = []
        [result.extend(cls._spotify_connection.audio_features(tracks_ids[i : i + Constants.spotify_limit])) for i in range(0, len(tracks_ids), Constants.spotify_limit)]
        return result

    @classmethod
    def _execute_spotify_command(cls, command, args = [], kwargs = {}) -> list:
        result = []

        partial_result = command(cls._spotify_connection, *args, **kwargs)
        result = result + [item for item in partial_result['items']]

        while(partial_result['next']):
            partial_result = spotipy.client.Spotify.next(cls._spotify_connection, partial_result)
            result = result + [item for item in partial_result['items']]

        return result

    @classmethod
    def _normalize_features(cls, denormalized_features: dict) -> tuple:
        song_id = denormalized_features['id']
        normalized_features = [
                denormalized_features['acousticness'],
                denormalized_features['danceability'],
                denormalized_features['energy'],
                denormalized_features['instrumentalness'],
                denormalized_features['speechiness'],
                min(float(denormalized_features['tempo'])/500, 1),
                denormalized_features['valence']
                ]
        return song_id, normalized_features

    @classmethod
    def create_playlist(cls, name, ids):
        # Primeiramente, cria-se a playlist
        payload1 = {
                "name" : name
                }

        response = cls._spotify_connection._post("https://api.spotify.com/v1/users/{}/playlists".format(Constants.spotify_username), payload = payload1)
        playlist_id = response['id']

        # Adição das músicas à playlist
        uris_to_new_playlist = ["spotify:track:" + item for item in ids]
        payload2 = {
                "uris" : uris_to_new_playlist
                }

        cls._spotify_connection._post("https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id), payload = payload2)
