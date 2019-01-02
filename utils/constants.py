class Constants:
    spotify_limit = None
    local_library_filename = None
    features_names = ["acousticness", "danceability", "duration", "energy", "instrumentalness", "key_and_mode", "liveness", "loudness", "speechiness", "tempo", "time_signature", "valence"]

    @classmethod
    def init(cls):
        fd = open(".settings.ss", "r")
        for line in fd:
            key, value = line.rstrip().split("=")
            setattr(cls, key, value)

        cls.spotify_limit = 50
        cls.local_library_filename = "library_mirror.csv"
