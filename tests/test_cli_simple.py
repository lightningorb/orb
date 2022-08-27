# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-12 08:20:45
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-27 10:06:52

from .cli_test_case import CLITestCase
from orb.cli import invoice
from orb.cli import chain


def pytest_generate_tests(metafunc):
    if "c" in metafunc.fixturenames:
        metafunc.parametrize(
            "c", [("rest", "cln"), ("rest", "lnd"), ("grpc", "lnd")], indirect=True
        )


class TestCLISimple(CLITestCase):
    def test_cli_chain_fees(self, c, capsys):
        chain.fees(c)
        out = capsys.readouterr().out
        print(out)
        assert "fastestFee" in out

    # def test_cli_lnurl_generate(self):
    #     invoice.lnurl_generate(
    #         self.c,
    #         total_amount_sat=1,
    #         chunks=1,
    #         num_threads=1,
    #         url="LNURL1DP68GURN8GHJ7AMPD3KX2AR0VEEKZAR0WD5XJTNRDAKJ7TNHV4KXCTTTDEHHWM30D3H82UNVWQHHVCTVD9J8QCTJV4H8GV3CMHGV0A",
    #         wait=False,
    #     )
