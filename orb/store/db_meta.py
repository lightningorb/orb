from functools import lru_cache
from peewee import *
from kivy.app import App
from playhouse.sqlite_ext import *
import os

path_finding_db_name = "path_finding"
aliases_db_name = "aliases"
invoices_db_name = "invoices"
forwarding_events_db_name = "forwarding_events_v2"
htlcs_db_name = "htlcs"


@lru_cache(None)
def get_db(name):
    user_data_dir = App.get_running_app().user_data_dir
    path = os.path.join(user_data_dir, f"{name}.db")
    return SqliteExtDatabase(path)
