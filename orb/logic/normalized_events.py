# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-27 04:55:17
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-21 15:31:33

from dataclasses import dataclass
from orb.math.normal_distribution import NormalDistribution
from orb.lnd import Lnd


class ChanRoutingData:
    """
    Simple dataclass that holds data for
    normal distribution calculation.
    """

    def __init__(self, alias, chan_id, vals):
        self.alias = alias
        self.chan_id = chan_id
        self.vals = vals


class Event:
    """
    Simple dataclass that holds an Event for
    normal distribution calculation.
    """

    def __init__(self, amt, ppm):
        self.amt = amt
        self.ppm = ppm

    def __lt__(self, other):
        return self.ppm < other.ppm

    def __hash__(self):
        return self.ppm


def get_descritized_routing_events(c):
    from orb.store import model

    fh = (
        model.ForwardEvent()
        .select()
        .where(model.ForwardEvent.chan_id_out == str(c.chan_id))
    )

    # compute the PPMs
    events = sorted(
        [
            Event(
                amt=f.amt_in,
                ppm=int(((f.fee_msat / f.amt_in_msat) * 1_000_000_000) / 1_000),
            )
            for f in fh
        ]
    )

    norm_vals = []
    for e in events:
        for n in range(int(e.amt / 10_000)):
            norm_vals.append(Event(ppm=e.ppm, amt=10_000))

    alias = Lnd().get_node_alias(c.remote_pubkey)

    # make sure we have more than one event
    if len(set(norm_vals)) >= 2:
        return ChanRoutingData(
            chan_id=str(c.chan_id),
            vals=norm_vals,
            alias=alias,
        )


def get_normal_distribution(c):
    chan_routing_data = get_descritized_routing_events(c)
    if chan_routing_data:
        nd = NormalDistribution()
        nd.data = [x.ppm for x in chan_routing_data.vals]
        nd.calculate_prob_dist()
        return nd


def get_best_fee(c, include_zero):
    """
    Get the most frequent fee-rate. If include_zero is False
    then filter out 0 ppms
    """
    nd = get_normal_distribution(c)
    if nd:
        dist = nd.probability_distribution
        probs = [
            x["probability"] for x in dist if not include_zero and x["probability"] != 0
        ]
        return max(dist, key=lambda x: probs)["value"]
