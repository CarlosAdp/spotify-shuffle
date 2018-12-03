import spotipy

sp = spotipy.Spotify(auth = "BQCd2sB__aaTk0hH_nP35s8eflYm8gzxWhaJMKGka14z3iTPyOPT6cQIYbBznKWtP2jnHb1EpjhZnEiREQTzMdKvOIHHhtHSmwtP6MnC-W5nUoo8CFe6wAgXDc2R5PeKAtegr9zMNhug7LoTl2Y0fxAaWjoJ-mFyXhXaEQ1I_fTSMXqgsqV4lyEulbzYkbWTbCzKMGdtvyk3APqmfuqKYK2zajVUyOQJhTnb71GLQ_ql1aNrjpjb0QD7yq_M-h9w8Syf0PG-thG54JsjvJm7nOx7c_fvj72AqQQqIoo")

"""
results = sp.current_user_saved_tracks(limit = 50)
for item in results['items']:
    print(item['track']['id'], item['track']['name'])

while(results['next']):
    results = sp.next(results)
    for item in results['items']:
        print(item['track']['id'], item['track']['name'])

"""
