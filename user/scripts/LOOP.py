# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-01 11:17:57
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-07 08:03:14

from orb.lnd import Lnd
import requests

from orb.misc.plugin import Plugin


class LOOP(Plugin):
    def main(self):
        """
        Open a channel to LOOP with as much as the chain balance as possible.
        Floor to the nearest 10M.

        Fee: use mempool's fastest + 1 sat/vb
        """
        lnd = Lnd()

        LOOP_ADDRESS = "021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d@50.112.125.89:9735"
        LOOP, ADDRESS = LOOP_ADDRESS.split("@")

        try:
            lnd.connect(LOOP_ADDRESS)
        except:
            print("already connect")

        fastest = requests.get(f"https://mempool.space/api/v1/fees/recommended").json()[
            "fastestFee"
        ]
        assert fastest >= 1

        balance = int(lnd.get_balance().confirmed_balance / 10_000_000) * 10_000_000

        if balance >= 10_000_000:
            print(f"Opening a {balance:,} sat channel with LOOP")
            response = lnd.open_channel(
                node_pubkey_string=LOOP, sat_per_vbyte=fastest + 1, amount_sat=balance
            )
            print(response)

    @property
    def menu(self):
        return "open > LOOP"

    @property
    def uuid(self):
        return "29873ca1-f74e-4cc0-85c7-a8695c14f8d6"
