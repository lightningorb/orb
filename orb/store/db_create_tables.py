# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-30 10:04:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-19 04:59:46

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


def create_path_finding_tables():
    db = get_db(path_finding_db_name)
    try:
        db.create_tables([Payment, Attempt, Hop])
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
