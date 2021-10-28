from kivy.app import App
from peewee import *
import os
from functools import lru_cache

@lru_cache(None)
def get_db(name):
	user_data_dir = App.get_running_app().user_data_dir
	path = os.path.join(user_data_dir, f'{name}.db')
	db = SqliteDatabase(path)
	return db

class FowardEvent(Model):
	timestamp = TimestampField()
	chan_id_in = IntegerField()
	chan_id_out = IntegerField()
	amt_in = IntegerField()
	amt_out = IntegerField()
	fee = IntegerField()
	fee_msat = IntegerField()
	amt_in_msat = IntegerField()
	amt_out_msat = IntegerField()
	timestamp_ns = IntegerField()

	class Meta:
		database = get_db('fowarding_events')

def create_tables(name):
	db = get_db(name)
	try:
		db.create_tables([FowardEvent])
	except:
		pass