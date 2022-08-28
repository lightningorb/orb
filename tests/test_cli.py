# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-10 07:01:18
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-28 06:21:53

import re
from .cli_test_case import CLITestCase
from orb.cli import node
from orb.cli import chain
from orb.cli import invoice
from orb.cli import peer


def pytest_generate_tests(metafunc):
    if "pubkey" in metafunc.fixturenames:
        metafunc.parametrize(
            "pubkey", [("cln", "rest"), ("lnd", "rest"), ("lnd", "grpc")], indirect=True
        )


class TestCLI(CLITestCase):
    def test_cli_balance(self, pubkey, capsys):
        if self.impl == "cln":
            print("Not Implemented")
            return
        node.balance(pubkey=pubkey)
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

    def test_cli_info(self, pubkey, capsys):
        node.info(pubkey=pubkey)
        assert "num_peers" in capsys.readouterr().out

    def test_cli_chain_deposit(self, pubkey, capsys):
        chain.deposit(pubkey=pubkey)
        assert "deposit_address" in capsys.readouterr().out

    def test_cli_send(self, pubkey, capsys):
        chain.deposit(pubkey=pubkey)
        deposit = capsys.readouterr().out
        address = re.search(r"deposit_address\s+(.*)", deposit).group(1).strip()
        chain.send(pubkey=pubkey, address=address, amount=1000, sat_per_vbyte=1)
        send = capsys.readouterr().out
        assert any(x in send for x in ["txid", "error", "insufficient"])

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
