# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-30 10:04:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-06 08:52:44

from orb.store.db_meta import *
from orb.store.model import *


def create_invoices_tables():
    db = get_db(invoices_db_name)
    try:
        db.create_tables([Invoice])
    except:
        pass


def create_fowarding_tables():
    db = get_db(forwarding_events_db_name)
    try:
        db.create_tables([FowardEvent])
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
