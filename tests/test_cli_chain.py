# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-10 07:01:18
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-31 19:44:05

import re
from .cli_test_case import CLITestCase
from orb.cli import chain


def pytest_generate_tests(metafunc):
    if "pubkey" in metafunc.fixturenames:
        metafunc.parametrize(
            "pubkey", [("cln", "rest"), ("lnd", "rest"), ("lnd", "grpc")], indirect=True
        )


class TestCLI(CLITestCase):
    def test_cli_chain_deposit(self, pubkey, capsys):
        chain.deposit(pubkey=pubkey)
        assert "deposit_address" in capsys.readouterr().out

    def test_cli_chain_balance(self, pubkey, capsys):
        chain.balance(pubkey=pubkey)
        out = capsys.readouterr().out
        assert "confirmed_balance" in out
        assert "total_balance" in out
        assert "unconfirmed_balance" in out

    def test_cli_send(self, pubkey, capsys):
        chain.deposit(pubkey=pubkey)
        deposit = capsys.readouterr().out
        address = re.search(r"deposit_address\s+(.*)", deposit).group(1).strip()
        chain.send(pubkey=pubkey, address=address, satoshi=1000, sat_per_vbyte=1)
        send = capsys.readouterr().out
        assert any(x in send for x in ["txid", "error", "insufficient"])
