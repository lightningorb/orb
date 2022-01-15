# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-01 08:23:35
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-15 16:23:01

from pathlib import Path

from kivy.storage.jsonstore import JsonStore
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher

from orb.store.db_meta import *
from orb.misc.channels import Channels
from orb.lnd.lnd import Lnd
from orb.misc.utils import pref


class DataManager(EventDispatcher):
    """
    The DataManager class is a bit of an unfortunate
    singleton. There's a bunch of data we need to access
    from all over the application.

    It would be better for it not to be singleton, as
    that makes testing difficult, allegidly.
    """

    show_chords = BooleanProperty(False)
    show_chord = NumericProperty(0)
    chords_direction = NumericProperty(0)
    channels_widget_ux_mode = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        """
        DataManager class initializer.
        """
        super(DataManager, self).__init__(*args, **kwargs)
        self.menu_visible = False
        self.disable_shortcuts = False
        self.lnd = Lnd()

        self.channels = Channels(self.lnd)

        user_data_dir = App.get_running_app().user_data_dir
        self.store = JsonStore(Path(user_data_dir) / pref("path.json") / "orb.json")
        from orb.store import db_create_tables

        for db in [
            forwarding_events_db_name,
            path_finding_db_name,
            aliases_db_name,
            invoices_db_name,
            htlcs_db_name,
        ]:
            try:
                get_db(db).connect()
            except:
                # most likely already connected
                pass

        db_create_tables.create_path_finding_tables()
        db_create_tables.create_fowarding_tables()
        db_create_tables.create_aliases_tables()
        db_create_tables.create_invoices_tables()

    @property
    def cert_path(self):
        """
        Get the cert path, as specified by our user config.
        """
        user_data_dir = App.get_running_app().user_data_dir
        return (Path(user_data_dir) / pref("path.cert") / "tls.cert").as_posix()

    def save_cert(self, cert):
        """
        Save the certificate to an file. This is required for
        requests over rest.
        """
        user_data_dir = App.get_running_app().user_data_dir
        with open(DataManager().cert_path, "w") as f:
            f.write(cert)

    @staticmethod
    def ensure_cert():
        """
        Make sure the cert's formatting is kosher.
        """
        user_data_dir = App.get_running_app().user_data_dir
        with open(DataManager().cert_path, "w") as f:
            f.write(pref("lnd.tls_certificate"))


data_man = None
