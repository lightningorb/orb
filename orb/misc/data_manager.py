# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-01 08:23:35
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-23 19:58:02

from traceback import format_exc

from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.event import EventDispatcher

from orb.store.db_meta import *
from orb.misc.channels import Channels
from orb.lnd.lnd import Lnd


class DataManager(EventDispatcher):
    """
    The DataManager class is a bit of an unfortunate
    singleton. There's a bunch of data we need to access
    from all over the application.

    It was created before proper knowledge of Kivy. In fact
    this data can simply reside int he main app class.

    It would be better for it not to be singleton, as
    that makes testing difficult, allegedly.
    """

    pubkey = StringProperty("")
    show_chords = BooleanProperty(False)
    menu_visible = BooleanProperty(False)
    show_chord = NumericProperty(0)
    chords_direction = NumericProperty(0)
    channels_widget_ux_mode = NumericProperty(0)
    highlighter_updated = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        """
        DataManager class initializer.
        """
        super(DataManager, self).__init__(*args, **kwargs)
        self.menu_visible = False
        self.disable_shortcuts = False
        self.lnd = Lnd()
        try:
            self.pubkey = self.lnd.get_info().identity_pubkey
        except:
            print(format_exc())
            print("Error getting pubkey")

        self.plugin_registry = {}

        self.channels = Channels(self.lnd)

        from orb.store import db_create_tables

        dbs = [
            aliases_db_name,
            forwarding_events_db_name,
            invoices_db_name,
            htlcs_db_name,
            channel_stats_db_name,
            payments_db_name,
        ]
        for db in dbs:
            try:
                get_db(db).connect()
            except Exception as e:
                print(e)
                print(format_exc())
                print(f"issue connecting with: {db}")
                assert False

        db_create_tables.create_forwarding_tables()
        db_create_tables.create_aliases_tables()
        db_create_tables.create_invoices_tables()
        db_create_tables.create_htlcs_tables()
        db_create_tables.create_channel_stats_tables()
        db_create_tables.create_payments_tables()
        db_create_tables.create_path_finding_tables()

        for db in dbs:
            get_db(db).close()


data_man = None
