import csv
import random
import spotipy
from blist import blist

from utils.functions import get_song_distance, get_token, calculate_base_features, russian_roulette
from utils.constants import Constants

# Definição do nome do arquivo e dos pesos para calculo de distância entre músicas
filename = "library_mirror.csv"
weights = [3, 7, 0.5, 5, 1, 2, 1, 0.5, 1, 3, 0.5, 10]


if __name__ == "__main__":
    # Lendo CSV
    try:
        fd = open(filename, "r")
        csv_reader = csv.reader(fd, delimiter = ",")

        # Definição do mapeamento entre id de música e suas features (candidatos)
        infos = {}
        candidates = blist([])
        chosen_ids = []

        for row in csv_reader:
            infos.update({row[0]: [float(item) for item in row[1:]]})
            candidates.append(row[0])

        # Escolha da primeira música
        first_song_id = random.choice(candidates)
        chosen_ids.append(first_song_id)
        candidates.remove(first_song_id)

        # Escolha das outras 99
        for i in range(99):
            # Cálculo da "média" das últimas músicas escolhidas (pesos de 16 para a última, 8 para a anterior, 4, 2 e 1, sucessivamente)
            base_features = calculate_base_features(chosen_ids, infos)
            closed_candidates = sorted(candidates, key = lambda item : get_song_distance(infos[item], base_features, weights))[:int(len(candidates)/20)]
            print(len(closed_candidates))

            next_id = russian_roulette(closed_candidates, key = lambda item: 1 / (0.00000001 + get_song_distance(base_features, infos.get(item), weights)))
            chosen_ids.append(next_id)
            candidates.remove(next_id)

        differences = [get_song_distance(infos.get(i1), infos.get(i2), weights) for i1, i2 in zip(chosen_ids, chosen_ids[1:])]

        # Formatação da URL para criação da playlist
        Constants.init()
        payload1 = {
                'name': 'shuffle_{}'.format(first_song_id)
                }
        sp = spotipy.Spotify(get_token())
        response = sp._post("https://api.spotify.com/v1/users/{}/playlists".format(Constants.username), payload = payload1)
        playlist_id = response['id']

        # Formatação de URL para adição de músicas à playlist recém criada
        uris_to_new_playlist = ["spotify:track:" + item for item in chosen_ids]
        payload2 = {
                'uris': uris_to_new_playlist
                }

        sp._post("https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id), payload = payload2)

    except FileNotFoundError:
        print("Arquivo não encontrado. Atualize o espelho de sua biblioteca do Spotify")
