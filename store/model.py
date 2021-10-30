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


def create_fowarding_tables():
    db = get_db('fowarding_events')
    try:
        db.create_tables([FowardEvent])
    except:
        pass


class Payment(Model):
    amount = IntegerField()
    dest = CharField()
    fees = IntegerField()
    succeeded = BooleanField()
    timestamp = TimestampField()

    class Meta:
        database = get_db('path_finding')


class Attempt(Model):
    code = IntegerField()
    weakest_link_pk = CharField()
    succeeded = BooleanField()
    payment = ForeignKeyField(Payment, backref='attempts')

    class Meta:
        database = get_db('path_finding')


class Hop(Model):
    pk = CharField()
    succeeded = BooleanField()
    attempt = ForeignKeyField(Attempt, backref='hops')

    class Meta:
        database = get_db('path_finding')


def create_path_finding_tables():
    db = get_db('path_finding')
    try:
        db.create_tables([Payment, Attempt, Hop])
    except:
        pass


class Node(Model):
    pk = CharField()
    successes = IntegerField()
    failures = IntegerField()
    rank = IntegerField()

    class Meta:
        database = get_db('node_rank')


def create_node_rank_tables():
    db = get_db('node_rank')
    try:
        db.create_tables([Node])
    except:
        pass


class Alias(Model):
    pk = CharField()
    alias = CharField()

    class Meta:
        database = get_db('aliases')


def create_aliases_tables():
    db = get_db('aliases')
    try:
        db.create_tables([Alias])
    except:
        pass
