import csv
import spotipy
from utils.functions import get_token, execute_spotify_command, normalize_features
from utils.constants import Constants

filename = "library_mirror.csv"
limit = 50
print("A")

if __name__ == "__main__":
    # Abrindo CSV
    try:
        fd = open(filename, "r")

        csv_reader = csv.reader(fd, delimiter = ',')
        old_library = []
        for row in csv_reader:
            old_library.append(row)

        # Armazenando ids registrados no espelho local
        local_id_list = list(list(zip(*old_library))[0])
    except FileNotFoundError:
        local_id_list = []
    except IndexError:
        local_id_list = []

    # recuperando ids de faixas da biblioteca remota
    Constants.init()
    sp = spotipy.Spotify(
            auth = get_token())

    tracks_info = execute_spotify_command(sp, spotipy.client.Spotify.current_user_saved_tracks, (limit, ))
    remote_id_list = [item['track']['id'] for item in tracks_info]

    # Definição de ids para inserção e deleção
    ids_to_insert = [item for item in remote_id_list if item not in local_id_list]
    ids_to_delete = [item for item in local_id_list if item not in remote_id_list]

    # Extração de features para novas inserções
    ids_to_insert_split_in_chunks = [ids_to_insert[i : i + limit] for i in range(0, len(ids_to_insert), limit)]
    features_denormalized = []
    for ids in ids_to_insert_split_in_chunks:
        features_denormalized = features_denormalized + sp.audio_features(tracks=ids)

    # Normalizando as features
    features_normalized = [normalize_features(item) for item in features_denormalized]

    # Atualizando o arquivo csv
    fd = open(filename, "w")
    csv_writer = csv.writer(fd)

    if len(local_id_list) > 0:
        for row in old_library:
            if row[0] not in ids_to_delete:
                csv_writer.writerow(row)

    for features in features_normalized:
        csv_writer.writerow([features[0]] + list(features[1]))
