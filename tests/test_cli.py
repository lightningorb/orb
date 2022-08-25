# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-10 07:01:18
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-23 07:05:16

import re
from nose.tools import *
from parameterized import parameterized_class
from .cli_test_case import CLITestCase, get_params
from orb.cli import node
from orb.cli import chain
from orb.cli import invoice
from orb.cli import peer


"""
Running all tests in this file:
$ nosetests tests.test_cli
Running cli_balance for cln rest only:
$ nosetests tests.test_cli:TestCLI_2_cln_rest.test_cli_balance
$ nosetests tests.test_cli:TestCLI_1_lnd_grpc.test_cli_send --nocapture
$ nosetests tests.test_cli:TestCLI_2_cln_rest.test_cli_send --nocapture
$ nosetests tests.test_cli:TestCLI_2_cln_rest.test_cli_send --nocapture
"""


@parameterized_class(*get_params())
class TestCLI(CLITestCase):
    def test_cli_balance(self):
        if self.impl == "cln":
            self.skipTest("Not Implemented")
        out = self.c.run("env ORB_CLI_NO_COLOR=1 ./main.py node.balance").stdout
        assert_true(int(out) > 1)

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

    def test_cli_info(self):
        node.info(self.c)
        assert_true("num_peers" in self.stdout)

    def test_cli_chain_deposit(self):
        chain.deposit(self.c)
        assert_true("deposit_address" in self.stdout)

    def test_cli_send(self):
        chain.deposit(self.c)
        deposit = self.get_stdout(flush=True)
        address = re.search(r"deposit_address\s+(.*)", deposit).group(1).strip()
        chain.send(self.c, address=address, amount=1000, sat_per_vbyte=1)
        send = self.get_stdout(flush=True)
        self.stop_capture()
        assert_true(any(x in send for x in ["txid", "error", "insufficient"]))

    def test_cli_invoice_generate(self):
        invoice.generate(self.c)
        assert_true("deposit_qr" in self.stdout)

    def test_peer_list(self):
        # nosetests tests.test_cli:TestCLI_1_lnd_grpc.test_peer_list --nocapture
        # nosetests tests.test_cli:TestCLI_0_lnd_rest.test_peer_list --nocapture
        # nosetests tests.test_cli:TestCLI_2_cln_rest.test_peer_list --nocapture
        peer.list(self.c)
        self.stop_capture()
        peers = self.stdout.strip().split("\n")
        num = 0
        for p in peers:
            if len(p.strip()) == 66:
                num += 1
        assert_true(num >= 2)


if __name__ == "__main__":
    unittest.main()
