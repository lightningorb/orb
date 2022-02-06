# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 13:24:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-06 08:11:36
import os
import arrow
from peewee import *

from playhouse.hybrid import hybrid_property, hybrid_method
from playhouse.sqlite_ext import *

from kivy.app import App

from orb.store.db_meta import *


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
            f"{self.chan_id_in} -> {self.chan_id_out} on"
            f" {arrow.get(self.timestamp).format()} ({self.timestamp})"
        )

    class Meta:
        database = get_db(forwarding_events_db_name)


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
    payment = ForeignKeyField(Payment, backref="attempts")

    class Meta:
        database = get_db(path_finding_db_name)


class Hop(Model):
    pk = CharField()
    succeeded = BooleanField()
    attempt = ForeignKeyField(Attempt, backref="hops")

    class Meta:
        database = get_db(path_finding_db_name)


class Alias(Model):
    pk = CharField()
    alias = CharField()

    class Meta:
        database = get_db(aliases_db_name)


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


class Htlc(Model):
    incoming_channel_id = IntegerField(default=0)
    outgoing_channel_id = IntegerField(default=0)
    incoming_htlc_id = IntegerField(default=0)
    outgoing_htlc_id = IntegerField(default=0)
    timestamp = IntegerField(default=0)
    event_type = CharField()
    event_outcome = CharField()
    event_outcome_info = JSONField(
        default={
            "incoming_amt_msat": 0,
            "incoming_timelock": 0,
            "outgoing_amt_msat": 0,
            "outgoing_timelock": 0,
        }
    )
    link_fail_event = JSONField(default={})

    class Meta:
        db_table = "htlc"
        database = get_db(htlcs_db_name)
