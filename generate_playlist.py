from utils.manager import Manager
from utils.library import LocalLibrary

if __name__ == "__main__":
    Manager.init()
    Manager.prepare_candidates()
    Manager.mount_shuffled_playlist()
