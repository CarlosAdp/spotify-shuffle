from utils.constants import Constants
from spotipy.util import prompt_for_user_token
from pprint import pprint
from numpy import average
import random
import spotipy

function_type = type(prompt_for_user_token)

def get_token() -> str:
    token = prompt_for_user_token(username=Constants.username,
            scope=Constants.scopes,
            client_id=Constants.client_id,
            client_secret=Constants.client_secret,
            redirect_uri=Constants.redirect_uri)

    return token

def execute_spotify_command(spotify_instance, command, args = [], kwargs = {}) -> list:
    result = []

    partial_result = command(spotify_instance, args, *args, **kwargs)
    result = result + [item for item in partial_result['items']]

    while(partial_result['next']):
        partial_result = spotipy.client.Spotify.next(spotify_instance, partial_result)
        result = result + [item for item in partial_result['items']]

    return result

def normalize_features(denormalized_features: dict) -> tuple:
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
            float(denormalized_features['time_signature'])/18,
            denormalized_features['valence']
            ]
    return song_id, normalized_features

def get_song_distance(s1_features, s2_features, weight):
    return sum([w * (i1 - i2) * (i1 - i2) for w, i1, i2 in zip(weight, s1_features, s2_features)])

def calculate_base_features(chosen_ids: list, infos: dict) -> list:
    weights = [1, 2, 4, 8, 16]
    last_ids = chosen_ids[-5:]
    last_ids_features = [infos.get(id_) for id_ in last_ids]
    weights = weights[-1 * len(last_ids_features):]

    return average(last_ids_features, axis=0, weights=weights[-1 * len(last_ids_features):])

def russian_roulette(iterable, key):
    items_and_metrics = []
    metrics_sum = 0

    for item in iterable:
        metric = key(item)
        metrics_sum += metric

        items_and_metrics.append({
            'item': item,
            'metric': metric
            })

    reference_value = random.uniform(0, metrics_sum)
    reference_sum = 0

    for item_and_metric in items_and_metrics:
        reference_sum += item_and_metric.get("metric")
        if reference_sum > reference_value:
            return item_and_metric.get("item")
