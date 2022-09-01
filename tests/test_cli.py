# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-10 07:01:18
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-01 18:01:28

import re
from .cli_test_case import CLITestCase
from orb.cli import node
from orb.cli import invoice
from orb.cli import peer


def pytest_generate_tests(metafunc):
    if "pubkey" in metafunc.fixturenames:
        metafunc.parametrize(
            "pubkey", [("cln", "rest"), ("lnd", "rest"), ("lnd", "grpc")], indirect=True
        )


class TestCLI(CLITestCase):
    # def test_cli_rebalance(self):
    #     if self.impl == "cln":
    #         self.skipTest("Not Implemented")
    #     out = self.c.run(
    #         "./main.py rebalance.rebalance --fee-rate 5_000_000 --amount 1"
    #     ).stdout
    #     assert_true(
    #         any(
    #             [
    #                 x in out
    #                 for x in ["T0: SUCCESS", "No routes found", "No more routes found"]
    #             ]
    #         )
    #     )

    def test_cli_info(self, pubkey, capsys):
        node.info(pubkey=pubkey)
        assert "num_peers" in capsys.readouterr().out

    def test_cli_invoice_generate(self, pubkey, capsys):
        invoice.generate(pubkey=pubkey, satoshis=1000)
        assert "deposit_qr" in capsys.readouterr().out

    def test_peer_list(self, pubkey, capsys):
        peer.list(pubkey=pubkey)
        peers = capsys.readouterr().out.split("\n")
        num = 0
        for p in peers:
            if len(p.strip()) == 66:
                num += 1
        assert num >= 2
