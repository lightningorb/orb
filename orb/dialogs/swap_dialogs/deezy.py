# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-27 13:36:03
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-27 16:46:43

import requests
import json

from memoization import cached

from orb.misc.mempool import get_fees
from orb.misc.auto_obj import dict2obj


class Network:
    testnet = 0
    mainnet = 1


class Deezy:
    def __init__(self, mode: Network = Network.mainnet, version: str = "1"):
        self.mode: Network = mode
        self.version: str = version

    @property
    def __prefix(self) -> str:
        return ("api-testnet.", "api.")[self.mode == Network.mainnet]

    @property
    def __fqdn(self) -> str:
        return f"https://{self.__prefix}deezy.io"

    @property
    def __url(self) -> str:
        return f"{self.__fqdn}/v{self.version}"

    @cached(ttl=60)
    def info(self):
        return dict2obj(requests.get(f"{self.__url}/swap/info").json())

    def amount_sats_is_above_max(self, amount_sats: str):
        return amount_sats > self.info().max_swap_amount_sats

    def amount_sats_is_below_min(self, amount_sats: str):
        return amount_sats < self.info().min_swap_amount_sats

    def estimate_cost(self, amount_sats: int, fee_rate: int, mp_fee: int):
        r = self.info()
        if amount_sats < r.min_swap_amount_sats:
            print(f"Min amount is: {r.min_swap_amount_sats}")
            return
        if amount_sats > r.max_swap_amount_sats:
            print(f"Min amount is: {r.min_swap_amount_sats}")
            return
        routing_rate = amount_sats * fee_rate / 1e6
        deezy_liq_rate = amount_sats * r.liquidity_fee_ppm / 1e6
        deezy_chain_rate = mp_fee * r.on_chain_bytes_estimate
        total_fee = int(routing_rate + deezy_liq_rate + deezy_chain_rate)
        return total_fee

    def swap(self, amount_sats: int, address: str, mp_fee: int):
        url = f"{self.__url}/swap"
        doc = {
            "amount_sats": amount_sats,
            "on_chain_address": address,
            "on_chain_sats_per_vbyte": mp_fee,
        }
        return dict2obj(
            requests.post(
                f"{self.__url}/swap",
                headers={"content-type": "application/json"},
                data=json.dumps(doc),
            ).json()
        )
