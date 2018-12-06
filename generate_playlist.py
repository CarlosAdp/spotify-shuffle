import csv
import random
import spotipy

from utils.functions import get_song_distance, get_token
from utils.constants import Constants

# Definição do nome do arquivo e dos pesos para calculo de distância entre músicas
filename = "library_mirror.csv"
weights = [3, 5, 0.5, 5, 1, 3, 1, 0.5, 1, 3, 0.5, 10]


if __name__ == "__main__":
    # Lendo CSV
    try:
        fd = open(filename, "r")
        csv_reader = csv.reader(fd, delimiter = ",")

        # Definição do mapeamento entre id de música e suas features
        infos = {}
        songs_ids = []

        for row in csv_reader:
            infos.update({row[0]: [float(item) for item in row[1:]]})
            songs_ids.append(row[0])

        # Escolha da música base
        base_song_id = random.choice(songs_ids)
        songs_ids.remove(base_song_id)

        # Realiza o cálculo da distância somente entre até 1000 músicas aleatoriamente escolhidas dentro da biblioteca
        random.shuffle(songs_ids)
        candidates = songs_ids[:1000]

        # Escolha das 50 músicas mais parecidas com a música base
        sorted_songs_ids = sorted(songs_ids, key = lambda item : get_song_distance(infos[item], infos[base_song_id], weights))
        ids_to_new_playlist = [base_song_id] + sorted_songs_ids[:49]

        # Formatação da URL para criação da playlist
        Constants.init()
        payload1 = {
                'name': 'shuffle_{}'.format(base_song_id)
                }
        sp = spotipy.Spotify(get_token())
        response = sp._post("https://api.spotify.com/v1/users/{}/playlists".format(Constants.username), payload = payload1)
        playlist_id = response['id']

        # Formatação de URL para adição de músicas à playlist recém criada
        uris_to_new_playlist = ["spotify:track:" + item for item in ids_to_new_playlist]
        payload2 = {
                'uris': uris_to_new_playlist
                }

        sp._post("https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id), payload = payload2)

    except FileNotFoundError:
        print("Arquivo não encontrado. Atualize o espelho de sua biblioteca do Spotify")
