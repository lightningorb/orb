import os
from functools import lru_cache
import arrow
from peewee import *

from playhouse.hybrid import hybrid_property, hybrid_method

from kivy.app import App


path_finding_db_name = 'path_finding'
aliases_db_name = 'aliases'
invoices_db_name = 'invoices'
forwarding_events_db_name = 'forwarding_events_v2'


@lru_cache(None)
def get_db(name):
    user_data_dir = App.get_running_app().user_data_dir
    path = os.path.join(user_data_dir, f'{name}.db')
    return SqliteDatabase(path)


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

    @hybrid_method
    def this_week(self):
        return (self.timestamp + 3600 * 24 * 7) > arrow.now().timestamp()

    @hybrid_method
    def this_month(self):
        return (self.timestamp + 3600 * 24 * 30) > arrow.now().timestamp()

    @hybrid_method
    def today(self):
        """
           + --------------- + -----------------------> greater than
          ts                delta               now
          |                  |                   |
          v                  v                   v
        -------------------------------------------------

        """
        return (self.timestamp + 3600 * 24) > arrow.now().timestamp()

    def __str__(self):
        return (
            f'{self.chan_id_in} -> {self.chan_id_out} on'
            f' {arrow.get(self.timestamp).format()} ({self.timestamp})'
        )

    class Meta:
        database = get_db(forwarding_events_db_name)


def create_fowarding_tables():
    db = get_db(forwarding_events_db_name)
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
        database = get_db(aliases_db_name)


def create_aliases_tables():
    db = get_db(aliases_db_name)
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

    @hybrid_method
    def expired(self):
        """
                                               |
        ------|---------|-----------------------------------
              ts       ts + e
        """
        return (self.timestamp + self.expiry) < arrow.now().timestamp()

    class Meta:
        database = get_db(invoices_db_name)


def create_invoices_tables():
    db = get_db(invoices_db_name)
    try:
        db.create_tables([Invoice])
    except:
        pass
