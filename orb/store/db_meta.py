# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-30 10:04:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-30 09:53:13

from pathlib import Path
from functools import lru_cache

from playhouse.sqlite_ext import SqliteExtDatabase
from playhouse.sqliteq import SqliteQueueDatabase

from kivy.app import App

from orb.misc.utils import pref

path_finding_db_name = "path_finding"
payments_db_name = "payments_v2"
aliases_db_name = "aliases"
invoices_db_name = "invoices"
forwarding_events_db_name = "forwarding_events_v7"
channel_stats_db_name = "channel_stats_v2"
htlcs_db_name = "htlcs_v4"


class OrbSqliteExtDatabase(SqliteQueueDatabase):
    def connect(self):
        # print("=" * 50)
        # print(f"CONNECTING to {self}")
        super(OrbSqliteExtDatabase, self).connect()
        # print("-" * 50)

    def close(self):
        # print("=" * 50)
        # print(f"CLOSING {self}")
        super(OrbSqliteExtDatabase, self).close()
        # print("-" * 50)


@lru_cache(None)
def get_db(name):
    app = App.get_running_app()
    if app:
        path = Path(app.user_data_dir) / pref("path.db") / f"{name}.db"
        return OrbSqliteExtDatabase(path, autoconnect=False)
