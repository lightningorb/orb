# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-30 10:04:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-10 09:59:52

from pathlib import Path
from functools import lru_cache

from playhouse.sqliteq import SqliteQueueDatabase

path_finding_db_name = "path_finding_v2"
payments_db_name = "payments_v3"
aliases_db_name = "aliases"
invoices_db_name = "invoices"
forwarding_events_db_name = "forwarding_events_v8"
channel_stats_db_name = "channel_stats_v3"
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
    from orb.app import App
    from orb.misc.utils_no_kivy import pref

    app = App.get_running_app()
    if app:
        path = Path(app.user_data_dir) / pref("path.db") / f"{name}.db"
        return OrbSqliteExtDatabase(path, autoconnect=False)
