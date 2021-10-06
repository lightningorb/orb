from kivy.app import App
from kivy.storage.jsonstore import JsonStore
import os


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

        if not mock:
            try:
                self.lnd = Lnd(
                    config["lnd"]["tls_certificate"],
                    config["lnd"]["hostname"],
                    config["lnd"]["network"],
                    config["lnd"]["macaroon_admin"],
                )
            except:
                from mock_lnd import Lnd as MockLnd

                self.lnd = MockLnd()
        else:
            self.lnd = Lnd()

        user_data_dir = App.get_running_app().user_data_dir
        self.store = JsonStore(os.path.join(user_data_dir, "orb.json"))

    @property
    def cert_path(self):
        user_data_dir = App.get_running_app().user_data_dir
        return os.path.join(user_data_dir, "tls.cert")

    @staticmethod
    def save_cert(cert):
        user_data_dir = App.get_running_app().user_data_dir
        with open(os.path.join(user_data_dir, "tls.cert"), "w") as f:
            f.write(cert)


data_man = None
