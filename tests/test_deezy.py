# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-09 08:44:05
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-28 17:45:50

import unittest

from orb.dialogs.swap_dialogs.deezy import Deezy, Network


class TestDeezy(unittest.TestCase):
    def test_get_info(self):
        info = Deezy(mode=Network.testnet).info()
        eg = {
            "available": True,
            "liquidity_fee_ppm": 999,
            "max_swap_amount_sats": 20000000,
            "min_swap_amount_sats": 100000,
            "on_chain_bytes_estimate": 300,
        }
        self.assertEqual(sorted(info.__dict__.keys()), sorted(eg.keys()))

    def test_estimate_cost(self):
        deezy = Deezy(mode=Network.testnet)
        fr = deezy.estimate_cost(amount_sats=100_000, fee_rate=500, mp_fee=1)
        self.assertTrue(fr > 0)

    def test_swap(self):
        deezy = Deezy(mode=Network.testnet)
        r = deezy.swap(
            amount_sats=100_000,
            address="tb1qrcdhlm0mk5lp4r3lx3sjgg2avryp76v2lul3qc",
            mp_fee=1,
        )
        self.assertTrue("lntb" in r.bolt11_invoice)


if __name__ == "__main__":
    unittest.main()
