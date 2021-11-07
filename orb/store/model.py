import os
from functools import lru_cache
import arrow
from peewee import *
from kivy.app import App
from playhouse.hybrid import hybrid_property

path_finding_db_name = 'path_finding'


@lru_cache(None)
def get_db(name):
    user_data_dir = App.get_running_app().user_data_dir
    path = os.path.join(user_data_dir, f'{name}.db')
    db = SqliteDatabase(path)
    return db


class FowardEvent(Model):
    timestamp = IntegerField()
    chan_id_in = IntegerField()
    chan_id_out = IntegerField()
    amt_in = IntegerField()
    amt_out = IntegerField()
    fee = IntegerField()
    fee_msat = IntegerField()
    amt_in_msat = IntegerField()
    amt_out_msat = IntegerField()
    timestamp_ns = IntegerField()

    def __str__(self):
        return (
            f'{self.chan_id_in} -> {self.chan_id_out} on'
            f' {arrow.get(self.timestamp).format()} ({self.timestamp})'
        )

    class Meta:
        database = get_db('forwarding_events_v2')


def create_fowarding_tables():
    db = get_db('forwarding_events_v2')
    try:
        db.create_tables([FowardEvent])
    except:
        pass


class Payment(Model):
    amount = IntegerField()
    dest = CharField()
    fees = IntegerField()
    succeeded = BooleanField()
    timestamp = IntegerField()

    class Meta:
        database = get_db(path_finding_db_name)


class Attempt(Model):
    code = IntegerField()
    weakest_link_pk = CharField()
    succeeded = BooleanField()
    payment = ForeignKeyField(Payment, backref='attempts')

    class Meta:
        database = get_db(path_finding_db_name)


class Hop(Model):
    pk = CharField()
    succeeded = BooleanField()
    attempt = ForeignKeyField(Attempt, backref='hops')

    class Meta:
        database = get_db(path_finding_db_name)


def create_path_finding_tables():
    db = get_db(path_finding_db_name)
    try:
        db.create_tables([Payment, Attempt, Hop])
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


class Invoice(Model):
    raw = CharField()
    destination = CharField()
    num_satoshis = IntegerField()
    timestamp = IntegerField()
    expiry = IntegerField()
    description = CharField()
    paid = BooleanField(default=False)
    # in_flight = BooleanField(default=False)

    @hybrid_property
    def expired(self):
        """
                                               |
        ------|---------|-----------------------------------
              ts       ts + e
        """
        exp = (self.timestamp + self.expiry) < arrow.now().timestamp()
        return exp

    class Meta:
        database = get_db('invoices')


def create_invoices_tables():
    db = get_db('invoices')
    try:
        db.create_tables([Invoice])
    except:
        pass
