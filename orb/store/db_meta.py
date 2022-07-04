# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-30 10:04:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-02 18:48:31

from pathlib import Path
from functools import lru_cache

from playhouse.sqlite_ext import SqliteExtDatabase

from kivy.app import App

from orb.misc.utils import pref

path_finding_db_name = "path_finding"
payments_db_name = "payments_v2"
aliases_db_name = "aliases"
invoices_db_name = "invoices"
forwarding_events_db_name = "forwarding_events_v7"
channel_stats_db_name = "channel_stats_v2"
htlcs_db_name = "htlcs_v4"


@lru_cache(None)
def get_db(name):
    app = App.get_running_app()
    if app:
        path = Path(app.user_data_dir) / pref("path.db") / f"{name}.db"
        return SqliteExtDatabase(path)
