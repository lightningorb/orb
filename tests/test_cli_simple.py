# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-12 08:20:45
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-22 11:45:41

from nose.tools import *
from parameterized import parameterized_class
from .cli_test_case import names, CLITestCase
from orb.cli import invoice
from orb.cli import chain

"""
These tests do not vary based on implementation or protocol.

Running all tests in this file:

$ nosetests tests.test_cli_simple
"""


@parameterized_class(*[names, (("lnd_rest", "rest", "lnd"),)])
class TestCLISimple(CLITestCase):
    def test_cli_chain_fees(self):
        chain.fees(self.c)
        assert_true("fastestFee" in self.stdout)

    # def test_cli_lnurl_generate(self):
    #     invoice.lnurl_generate(
    #         self.c,
    #         total_amount_sat=1,
    #         chunks=1,
    #         num_threads=1,
    #         url="LNURL1DP68GURN8GHJ7AMPD3KX2AR0VEEKZAR0WD5XJTNRDAKJ7TNHV4KXCTTTDEHHWM30D3H82UNVWQHHVCTVD9J8QCTJV4H8GV3CMHGV0A",
    #         wait=False,
    #     )


if __name__ == "__main__":
    unittest.main()
