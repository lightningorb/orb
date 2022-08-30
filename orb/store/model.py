# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 13:24:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-30 11:47:56

import arrow

from playhouse.hybrid import hybrid_method
from playhouse.sqlite_ext import *

from orb.store.db_meta import *


class LNDPayment(Model):
    creation_date = IntegerField()
    creation_time_ns = IntegerField(unique=True)
    failure_reason = CharField()
    fee = IntegerField()
    fee_msat = IntegerField()
    fee_sat = IntegerField()
    payment_hash = CharField()
    payment_index = IntegerField()
    payment_preimage = CharField()
    payment_request = CharField()
    status = CharField()
    value = IntegerField()
    value_msat = IntegerField()
    value_sat = IntegerField()
    dest_pubkey = CharField()
    last_hop_pubkey = CharField()
    last_hop_chanid = IntegerField()
    first_hop_pubkey = CharField()
    first_hop_chanid = IntegerField()
    total_fees_msat = IntegerField()

    @hybrid_method
    def today(self):
        return (arrow.utcnow().timestamp() - self.creation_date) < 3600 * 24

    @hybrid_method
    def this_week(self):
        return (arrow.utcnow().timestamp() - self.creation_date) < 3600 * 24 * 7

    @hybrid_method
    def this_month(self):
        return (arrow.utcnow().timestamp() - self.creation_date) < 3600 * 24 * 30

    class Meta:
        database = get_db(payments_db_name)


class LNDPaymentAttempt(Model):
    attempt_id = IntegerField()
    attempt_time_ns = IntegerField()
    # failure = CharField()
    preimage = CharField()
    resolve_time_ns = IntegerField()
    status = CharField()
    payment = ForeignKeyField(LNDPayment, backref="htlcs")

    class Meta:
        database = get_db(payments_db_name)


class LNDAttemptRoute(Model):
    total_amt = IntegerField()
    total_amt_msat = IntegerField()
    total_fees = IntegerField()
    total_fees_msat = IntegerField()
    total_time_lock = IntegerField()
    attempt = ForeignKeyField(LNDPaymentAttempt, backref="route")

    class Meta:
        database = get_db(payments_db_name)


class LNDHop(Model):

    # amp_record = CharField(default="")
    amt_to_forward = IntegerField()
    amt_to_forward_msat = IntegerField()
    chan_capacity = IntegerField()
    chan_id = CharField()
    custom_records = JSONField(default={})
    expiry = IntegerField()
    fee = IntegerField()
    fee_msat = IntegerField()
    # mpp_record = JSONField(default={})
    pub_key = CharField()
    tlv_payload = BooleanField()
    route = ForeignKeyField(LNDAttemptRoute, backref="hops")

    class Meta:
        database = get_db(payments_db_name)


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


class ChannelStats(Model):
    chan_id = CharField(index=True, unique=True)
    earned_msat = IntegerField(default=0)
    helped_earn_msat = IntegerField(default=0)
    debt_msat = IntegerField(default=0)

    class Meta:
        database = get_db(channel_stats_db_name)


class ForwardEvent(Model):
    timestamp = IntegerField()
    chan_id_in = CharField()
    chan_id_out = CharField()
    amt_in = IntegerField()
    amt_out = IntegerField()
    fee = IntegerField()
    fee_msat = IntegerField()
    amt_in_msat = IntegerField()
    amt_out_msat = IntegerField()
    timestamp_ns = IntegerField(index=True, unique=False)

    @hybrid_method
    def this_week(self):
        return (arrow.utcnow().timestamp() - self.timestamp) < 3600 * 24 * 7

    @hybrid_method
    def this_month(self):
        return (arrow.utcnow().timestamp() - self.timestamp) < 3600 * 24 * 30

    @hybrid_method
    def today(self):
        return (arrow.utcnow().timestamp() - self.timestamp) < 3600 * 24

    def __str__(self):
        return (
            f"{self.chan_id_in} -> {self.chan_id_out} on"
            f" {arrow.get(self.timestamp).format()} ({self.timestamp})"
        )

    class Meta:
        database = get_db(forwarding_events_db_name)


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
