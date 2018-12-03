from utils.constants import Constants
from spotipy.util import prompt_for_user_token
import spotipy

class Manager:
    @classmethod
    def init(cls) -> None:
        return

    @classmethod
    def get_toke(cls) -> str:
        Constants.token = prompt_for_user_token(username=Constants.username,
                scope=Constants.scope,
                client_id=Constants.client_id,
                client_secret=Constants.client_secret,
                redirect_uri=Constants.redirect_uri)

        return Constants.token
