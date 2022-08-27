# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-10 07:01:18
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-27 09:52:38

from .cli_test_case import CLITestCase
from orb.ln import factory
from orb.cli.utils import get_default_id
from random import shuffle


def pytest_generate_tests(metafunc):
    if "c" in metafunc.fixturenames:
        metafunc.parametrize(
            "c", [("rest", "cln"), ("rest", "lnd"), ("grpc", "lnd")], indirect=True
        )


class TestAPI(CLITestCase):
    def test_get_route(self, c):
        ln = factory(get_default_id())
        channels = ln.get_channels()
        shuffle(channels)
        res = ln.get_route(
            pub_key=channels[-1].remote_pubkey,
            amount_sat=1,
            source_pub_key=channels[0].remote_pubkey,
            ignored_pairs=[],
            last_hop_pubkey="",
            outgoing_chan_id=None,
            fee_limit_msat=10_000_000,
        )
        assert res.total_amt == 1
        assert len(res.hops) > 0

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
