from kivy.app import App
from kivy.storage.jsonstore import JsonStore
import os


class DataManager:
    def __init__(self, config):
        self.init(config=config)

    def init(self, config):
        if config["lnd"]["protocol"] == "grpc":
            from lnd import Lnd as grpc_lnd

            self.lnd = grpc_lnd(
                config["lnd"]["tls_certificate"],
                config["lnd"]["hostname"],
                config["lnd"]["network"],
                config["lnd"]["macaroon_admin"],
            )
        elif config["lnd"]["protocol"] == "rest":
            from lnd_rest import Lnd as rest_lnd

            self.lnd = rest_lnd()
        elif config["lnd"]["protocol"] == "mock":
            from mock_lnd import Lnd as mock_lnd

            self.lnd = MockLnd()
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
