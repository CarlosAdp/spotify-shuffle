from utils.constants import Constants
from datetime import datetime
import random
from utils.library import LocalLibrary
from utils.lastfm import LastFmUtils
from utils.spotify_utils import SpotifyUtils
from numpy import average

class Manager:
    """
    Classe para realização de operações do sistema
    Sua inicialização é requisito necessário para funcionamento de qualquer script do projeto
    e envolve:
    - Inicialização de constantes
    - Carregamento da biblioteca local
    - Carregamento dos pesos utilizados na análise de proximidade
    """
    @classmethod
    def init(cls) -> None:
        Constants.init()
        LocalLibrary.load()
        cls.weights = [2, 4, 3, 1, 2, 1, 5]

    @classmethod
    def prepare_candidates(cls) -> None:
        cls.candidates_ids = list(LocalLibrary.data.index)
        cls.chosen_songs_ids = list()

    @classmethod
    def mount_shuffled_playlist(cls) -> None:
        # Escolhendo a primeira música
        first_song_candidates_ids = random.sample(cls.candidates_ids, 50)
        first_song_candidates_infos = LocalLibrary.get(ids=first_song_candidates_ids, columns=["artist", "album", "title"])
        first_song_candidates_time_metrics = [cls._calculate_time_metrics(data) for id, data in first_song_candidates_infos.iterrows()]

        first_song_id = first_song_candidates_ids[first_song_candidates_time_metrics.index(max(first_song_candidates_time_metrics))]

        cls.chosen_songs_ids.append(first_song_id)
        cls.candidates_ids.remove(first_song_id)

        while len(cls.chosen_songs_ids) < 50:
            next_song_id = cls._pick_next_song()
            cls.chosen_songs_ids.append(next_song_id)
            cls.candidates_ids.remove(next_song_id)

        SpotifyUtils.authenticate()
        SpotifyUtils.create_playlist(name="shuffle_{}".format(cls.chosen_songs_ids[0]), ids=cls.chosen_songs_ids)
        print(LocalLibrary.get(ids=cls.chosen_songs_ids))

    @classmethod
    def _calculate_time_metrics(cls, data) -> float:
        instants = LastFmUtils.get(data.artist, data.album, data.title)
        denominator = 1.0

        if instants is not None:
            now = datetime.now()

            for instant in instants:
                denominator += 1.0/(now - instant).total_seconds()

        return 1.0/denominator

    @classmethod
    def _pick_next_song(cls) -> str:
        base_features = cls._calculate_base_features()
        closest_twenty = sorted(cls.candidates_ids, key = lambda item : cls._get_song_distance(base_features, LocalLibrary.get(ids=[item], columns=Constants.features_names).values.tolist()[0], weight=cls.weights))[:5]
        closest_twenty_data = LocalLibrary.get(ids=closest_twenty)
        time_metrics = [cls._calculate_time_metrics(data) for id, data in closest_twenty_data.iterrows()]
        next_song_id = closest_twenty[time_metrics.index(max(time_metrics))]

        return next_song_id

    @classmethod
    def _calculate_base_features(cls) -> list:
        last_songs_ids = cls.chosen_songs_ids[-2:]
        weights = [1, 2][-1 * len(last_songs_ids):]
        last_ids_features = LocalLibrary.get(ids=last_songs_ids, columns=Constants.features_names)

        return average(last_ids_features, axis=0, weights=weights)

    @classmethod
    def _get_song_distance(cls, s1_features, s2_features, weight):
        return sum([w * (i1 - i2) * (i1 - i2) for w, i1, i2 in zip(weight, s1_features, s2_features)])
