from kivy.app import App
from kivy.storage.jsonstore import JsonStore
import os

controllers = {}


class DataManager:
    def __init__(self, config, mock=False):
        self.init(config=config, mock=mock)

    def init(self, config, mock=False):
        if not mock:
            try:
                from lnd import Lnd
            except:
                from mock_lnd import Lnd

                mock = True
        else:
            from mock_lnd import Lnd

        user_data_dir = App.get_running_app().user_data_dir

        self.store = JsonStore(os.path.join(user_data_dir, "orb.json"))
        if not mock:
            self.lnd = Lnd(
                os.path.expanduser(config["lnd"]["lnd_dir"]),
                config["lnd"]["hostname"],
                config["lnd"]["network"],
            )
        else:
            self.lnd = Lnd()


data_man = None
