from utils.constants import Constants
from utils.spotify_utils import SpotifyUtils
import pandas as pd

class LocalLibrary:
    """
    Classe que armazena os ids das músicas salvas no spotify e suas características (features)
    """
    features_names = Constants.features_names

    @classmethod
    def load(cls) -> None:
        """
        Carrega a biblioteca
        """
        try:
            cls.data = pd.read_csv(Constants.local_library_filename, sep='\t', index_col=0)
            cls.tracks_ids = list(cls.data.index)
        except FileNotFoundError:
            cls.data = pd.DataFrame(columns=
                    ["artist", "album", "title"] + cls.features_names)
            cls.tracks_ids = list()

    @classmethod
    def update(cls) -> None:
        user_tracks = SpotifyUtils.get_user_tracks()
        user_tracks_infos = dict()
        user_tracks_ids = list()

        for track in user_tracks:
            user_tracks_infos.update({
                track["id"] : [track["artists"][0]["name"], track["album"]["name"], track["name"]]
                })
            user_tracks_ids.append(track["id"])

        
        # Definição de ids para inserção e deleção
        ids_to_insert = [item for item in user_tracks_ids if item not in cls.tracks_ids]
        ids_to_delete = [item for item in cls.tracks_ids if item not in user_tracks_ids]

        cls.data = cls.data.drop(ids_to_delete)

        # Extração de features para novas inserções
        new_tracks_features = SpotifyUtils.get_tracks_features(ids_to_insert)
        normalized_features = [SpotifyUtils._normalize_features(item) for item in new_tracks_features]

        for track_id, track_features in normalized_features:
            cls.data.loc[track_id] = user_tracks_infos.get(track_id) + track_features

    @classmethod
    def save(cls) -> None:
        cls.data.to_csv(Constants.local_library_filename, sep='\t', encoding='utf-8')

    @classmethod
    def get(cls, ids=None, columns=None) -> list:
        if ids is None:
            if columns is None:
                return cls.data
            else:
                return cls.data[columns]
        else:
            if columns is None:
                return cls.data.loc[ids]
            else:
                return cls.data.loc[ids][columns]
