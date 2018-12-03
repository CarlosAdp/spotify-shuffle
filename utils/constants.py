class Constants:
    @classmethod
    def init(cls):
        fd = open(".config.ss", "r")
        for line in fd:
            key, value = line.rstrip().split("=")
            setattr(cls, key, value)

        cls.playlist_id = "1qGImNubYSgH7sBGlAdN9Y"
