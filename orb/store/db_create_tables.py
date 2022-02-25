# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-30 10:04:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-25 10:05:13

from orb.store.db_meta import *
from orb.store.model import *


def create_invoices_tables():
    db = get_db(invoices_db_name)
    try:
        db.create_tables([Invoice])
    except:
        pass


def create_forwarding_tables():
    db = get_db(forwarding_events_db_name)
    try:
        db.create_tables([ForwardEvent])
    except:
        pass


def create_aliases_tables():
    db = get_db(aliases_db_name)
    try:
        db.create_tables([Alias])
    except:
        pass


def create_htlcs_tables():
    db = get_db(htlcs_db_name)
    try:
        db.create_tables([Htlc])
        # qry = Htlc.delete().where(Htlc.timestamp >= 0)
        # qry.execute()
    except:
        pass


def create_channel_stats_tables():
    db = get_db(channel_stats_db_name)
    try:
        db.create_tables([ChannelStats])
    except:
        pass


def create_payments_tables():
    db = get_db(payments_db_name)
    try:
        db.create_tables([LNDPayment, LNDPaymentAttempt, LNDAttemptRoute, LNDHop])
    except:
        pass
