# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-10 10:18:30

import sys

from orb.ln import Ln


class Output:
    def __init__(self, ln: Ln):
        self.ln: Ln = ln

    def print_route(self, route):
        route_str = "\n".join(
            self.get_channel_representation(h.chan_id, h.pub_key)
            + "\t"
            + self.get_fee_information(h, route)
            for h in route.hops
        )
        print(route_str)

    def get_channel_representation(self, chan_id, pubkey_to, pubkey_from=None):
        channel_id_formatted = chan_id
        if pubkey_from:
            alias_to_formatted = format_alias(self.ln.get_node_alias(pubkey_to))
            alias_from = format_alias(self.ln.get_node_alias(pubkey_from))
            return f"{channel_id_formatted} ({alias_from} to {alias_to_formatted})"
        alias_to_formatted = format_alias(f"{self.ln.get_node_alias(pubkey_to):32}")
        return f"{channel_id_formatted} to {alias_to_formatted}"

    def get_fee_information(self, next_hop, route):
        hops = list(route.hops)
        if hops[0] == next_hop:
            ppm = self.ln.get_ppm_to(next_hop.chan_id)
            return f"(free, we usually charge {format_ppm(ppm)})"
        hop = hops[hops.index(next_hop) - 1]
        ppm = int(hop.fee_msat * 1_000_000 / hop.amt_to_forward_msat)
        fee_formatted = "fee " + f"{hop.fee_msat:8,} mSAT"
        ppm_formatted = format_ppm(ppm, 5)
        return f"({fee_formatted}, {ppm_formatted})"


def format_alias(alias):
    try:
        if sys.stdout.encoding and not sys.stdout.encoding.lower().startswith("utf"):
            alias = alias.encode("latin-1", "ignore").decode()
    except:
        pass
    return alias


def format_ppm(ppm, min_length=None):
    if min_length:
        return f"{ppm:{min_length},}ppm"
    return f"{ppm:,}ppm"


def format_earning(msat, min_width=None):
    if min_width:
        return f"{msat:{min_width},} mSAT"
    return f"{msat:,} mSAT"
