# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-10 07:01:18
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-27 09:39:13

import re
from .cli_test_case import CLITestCase
from orb.cli import node
from orb.cli import chain
from orb.cli import invoice
from orb.cli import peer


def pytest_generate_tests(metafunc):
    if "c" in metafunc.fixturenames:
        metafunc.parametrize(
            "c", [("rest", "cln"), ("rest", "lnd"), ("grpc", "lnd")], indirect=True
        )


class TestCLI(CLITestCase):
    def test_cli_balance(self, c, capsys):
        if self.impl == "cln":
            print("Not Implemented")
            return
        node.balance(c)
        assert int(capsys.readouterr().out) > 1

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

    def test_cli_info(self, c, capsys):
        node.info(c)
        assert "num_peers" in capsys.readouterr().out

    def test_cli_chain_deposit(self, c, capsys):
        chain.deposit(c)
        assert "deposit_address" in capsys.readouterr().out

    def test_cli_send(self, c, capsys):
        chain.deposit(c)
        deposit = capsys.readouterr().out
        address = re.search(r"deposit_address\s+(.*)", deposit).group(1).strip()
        chain.send(c, address=address, amount=1000, sat_per_vbyte=1)
        send = capsys.readouterr().out
        assert any(x in send for x in ["txid", "error", "insufficient"])

    def test_cli_invoice_generate(self, c, capsys):
        invoice.generate(c)
        assert "deposit_qr" in capsys.readouterr().out

    def test_peer_list(self, c, capsys):
        peer.list(c)
        peers = capsys.readouterr().out.split("\n")
        num = 0
        for p in peers:
            if len(p.strip()) == 66:
                num += 1
        assert num >= 2
