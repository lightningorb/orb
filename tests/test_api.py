# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-10 07:01:18
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-09 08:53:16

import logging
from .cli_test_case import CLITestCase
from orb.ln import factory
from orb.cli.utils import get_default_id
from random import shuffle


def pytest_generate_tests(metafunc):
    if "pubkey" in metafunc.fixturenames:
        metafunc.parametrize(
            "pubkey", [("cln", "rest"), ("lnd", "rest"), ("lnd", "grpc")], indirect=True
        )


class TestAPI(CLITestCase):
    def test_get_route(self, pubkey):
        ln = factory(pubkey)
        channels = ln.get_channels()
        shuffle(channels)
        dest_pubkey = channels[-1].remote_pubkey
        res = ln.get_route(
            pub_key=dest_pubkey,
            amount_sat=1,
            source_pub_key=None,
            ignored_pairs=[],
            last_hop_pubkey="",
            outgoing_chan_id=None,
            fee_limit_msat=10_000_000,
        )
        if res.hops:
            assert res.hops[-1].pub_key == dest_pubkey

    def test_get_circular_route(self, pubkey):
        ln = factory(pubkey)
        channels = ln.get_channels()
        shuffle(channels)
        our_pubkey = ln.get_info().identity_pubkey
        res = ln.get_route(
            pub_key=our_pubkey,
            amount_sat=1,
            source_pub_key=None,
            ignored_pairs=[],
            last_hop_pubkey=channels[0].remote_pubkey,
            outgoing_chan_id=channels[1].chan_id,
            fee_limit_msat=10_000_000,
        )
        if res.hops:
            assert res.hops[-1].pub_key == our_pubkey
        else:
            logging.warn("No circular route found")

    def get_channels(self, pubkey):
        ln = factory(pubkey)
        channels = ln.get_channels()
        assert len(channels) > 0
        for c in channels:
            assert type(c.chan_id) is str
            assert type(c.active) is bool
            assert type(c.local_balance) is int

    # def test_get_rebalance_route(self, c):
    #     pk = get_default_id()
    #     ln = factory(pk)
    #     channels = ln.get_channels()
    #     shuffle(channels)
    #     direction = int(pk < channels[0].remote_pubkey)
    #     ignored_nodes = [f"{channels[0].chan_id}/{direction}"]
    #     res = ln.get_route(
    #         pub_key=channels[0].remote_pubkey,
    #         ignored_nodes=ignored_nodes,
    #         amount_sat=1,
    #         ignored_pairs=[],
    #         last_hop_pubkey="",
    #         outgoing_chan_id=None,
    #         fee_limit_msat=10_000_000,
    #     )
    #     assert res.total_amt == 1
    #     assert len(res.hops) > 0
