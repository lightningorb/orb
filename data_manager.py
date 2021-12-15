# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-01 08:23:35
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-15 11:15:01

import os
from traceback import print_exc

from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher

from orb.store.db_meta import *
from orb.misc.channels import Channels


class DataManager(EventDispatcher):

    show_chords = BooleanProperty(False)
    show_chord = NumericProperty(0)
    chords_direction = NumericProperty(0)

    def __init__(self, config, *args, **kwargs):
        super(DataManager, self).__init__(*args, **kwargs)
        self.menu_visible = False
        self.disable_shortcuts = False
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

        self.channels = Channels(self.lnd)

        user_data_dir = App.get_running_app().user_data_dir
        self.store = JsonStore(os.path.join(user_data_dir, "orb.json"))
        from orb.store import db_create_tables
        from orb.logic.htlc import create_htlcs_tables

        get_db(forwarding_events_db_name).connect()
        get_db(path_finding_db_name).connect()
        get_db(aliases_db_name).connect()
        get_db(invoices_db_name).connect()
        get_db(htlcs_db_name).connect()

        db_create_tables.create_path_finding_tables()
        db_create_tables.create_fowarding_tables()
        db_create_tables.create_aliases_tables()
        db_create_tables.create_invoices_tables()
        create_htlcs_tables()

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
