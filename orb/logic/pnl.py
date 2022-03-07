# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-23 10:44:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-03-07 12:12:36

from collections import defaultdict
from operator import or_
import datetime
from orb.store.model import ForwardEvent, LNDPayment
import sys


def pnl(chan_id, liquidity=False):
    h, edges, liq = [], [], 0
    fh, fedges = [], []
    fee = 0
    cid = chan_id
    events = defaultdict(int)
    fee_events = defaultdict(int)
    total_sent, total_received = 0, 0
    for e in (
        ForwardEvent()
        .select()
        .where(or_(ForwardEvent.chan_id_in == cid, ForwardEvent.chan_id_out == cid))
    ):
        if e.chan_id_in == cid:
            events[e.timestamp_ns] = e.amt_in_msat
            total_received += e.amt_in_msat
        elif e.chan_id_out == cid:
            events[e.timestamp_ns] = -e.amt_out_msat
            fee_events[e.timestamp_ns] = e.fee_msat
            total_sent += e.amt_out_msat
    for e in (
        LNDPayment()
        .select()
        .where(
            or_(
                LNDPayment.first_hop_chanid == cid,
                LNDPayment.last_hop_chanid == cid,
            )
        )
    ):
        if e.first_hop_chanid == cid:
            events[e.creation_time_ns] = -e.value_msat
            total_sent += e.value_msat
        elif e.last_hop_chanid == cid:
            events[e.creation_time_ns] = e.value_msat
            fee_events[e.creation_time_ns] = -e.fee_msat
            total_received += e.value_msat

    for e in sorted([*events.keys()]):
        liq += events[e]
        edges.append(datetime.datetime.fromtimestamp(e / 1_000_000_000))
        h.append(liq)

    for e in sorted([*fee_events.keys()]):
        fee += fee_events[e]
        fedges.append(datetime.datetime.fromtimestamp(e / 1_000_000_000))
        fh.append(fee)

    if edges:
        edges.append(edges[-1])
    else:
        print("No data")
        return

    if fedges:
        fedges.append(fedges[-1])
    else:
        print("No data")
        return

    if liquidity:
        return h, edges

    return h, edges, fh, fedges
