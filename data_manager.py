from kivy.app import App
from kivy.storage.jsonstore import JsonStore
import os
from traceback import print_exc


class DataManager:
    def __init__(self, config):
        self.init(config=config)

    def init(self, config):
        self.menu_visible = False
        if config["lnd"]["protocol"] == "grpc":
            try:
                from orb.lnd.lnd import Lnd as grpc_lnd

                self.lnd = grpc_lnd(
                    config["lnd"]["tls_certificate"],
                    config["lnd"]["hostname"],
                    config["lnd"]["network"],
                    config["lnd"]["macaroon_admin"],
                )
            except:
                print(print_exc())
                from orb.lnd.mock_lnd import Lnd as mock_lnd

                self.lnd = mock_lnd()
        elif config["lnd"]["protocol"] == "rest":
            from orb.lnd.lnd_rest import Lnd as rest_lnd

            self.lnd = rest_lnd()
        elif config["lnd"]["protocol"] == "mock":
            from orb.lnd.mock_lnd import Lnd as mock_lnd

            self.lnd = mock_lnd()
        user_data_dir = App.get_running_app().user_data_dir
        self.store = JsonStore(os.path.join(user_data_dir, "orb.json"))
        from orb.store import model

        model.get_db('forwarding_events_v2').connect()
        model.get_db('path_finding').connect()
        model.get_db('aliases').connect()
        model.create_path_finding_tables()
        model.create_fowarding_tables()
        model.create_aliases_tables()

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
