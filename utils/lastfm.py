import requests
import json
from utils.constants import Constants
from datetime import datetime
from pprint import pprint

class LastFmUtils:
    songs_infos = dict()

    @classmethod
    def get(cls, artist, album, title):
        if artist not in cls.songs_infos.keys():
            cls._retrieve_artist_information(artist)

        try:
            result = cls.songs_infos.get(artist).get(album).get(title)
            return result
        except AttributeError:
            return None

    @classmethod
    def _retrieve_artist_information(cls, artist):
        page_number = 1
        result = dict()

        while True:
            response = requests.get("http://ws.audioscrobbler.com/2.0/?method=user.getartisttracks&user={}&artist={}&api_key={}&format=json&page={}".format(Constants.lastfm_username, artist, Constants.lastfm_api_key, page_number))
            info = response.json().get("artisttracks").get("track")

            if len(info) == 0:
                break

            for item in info:
                album = item.get("album").get("#text")
                title = item.get("name")

                if album not in result.keys():
                    result.update({
                        album : dict()
                        })

                if title not in result.get(album).keys():
                    result.get(album).update({
                        title : list()
                        })

                result.get(album).get(title).append(datetime.strptime(item.get("date")["#text"], "%d %b %Y, %H:%M"))

            page_number += 1

        cls.songs_infos.update({
            artist : result
            })
