# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-14 11:44:10

import codecs
import re
from typing import Union


class ClnBase:
    def __init__(self, protocol):
        self.protocol = protocol

    def get_alias_from_channel_id(self, chan_id) -> Union[str, None]:
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return self.get_node_alias(channel.remote_pubkey)

    @staticmethod
    def hex_string_to_bytes(hex_string: str) -> bytes:
        decode_hex = codecs.getdecoder("hex_codec")
        return decode_hex(hex_string)[0]

    def get_own_alias(self) -> str:
        return self.get_info().alias

    def get_version(self) -> str:
        if self.version:
            return self.version
        version = self.get_info().version
        self.version = re.search(r"(\d+\.\d+.\d+)+", version).group(1)
        return self.version

    def select_outputs_for_amount(self, satoshis: int):
        def select_outputs_greedy(unspent, min_value):
            """
            https://www.oreilly.com/library/view/mastering-bitcoin/9781491902639/ch05.html
            """
            # Fail if empty.
            if not unspent:
                return None, 0
            # Partition into 2 lists.
            lessers = [utxo for utxo in unspent if utxo.value < min_value]
            greaters = [utxo for utxo in unspent if utxo.value >= min_value]
            key_func = lambda utxo: utxo.value
            if greaters:
                # Not-empty. Find the smallest greater.
                min_greater = min(greaters, key=key_func)
                change = min_greater.value - min_value
                return [min_greater], change
            # Not found in greaters. Try several lessers instead.
            # Rearrange them from biggest to smallest. We want to use the least
            # amount of inputs as possible.
            lessers.sort(key=key_func, reverse=True)
            result = []
            accum = 0
            for utxo in lessers:
                result.append(utxo)
                accum += utxo.value
                if accum >= min_value:
                    change = accum - min_value
                    return result, change
            # No results found.
            return None, 0

        class OutputInfo:
            def __init__(self, tx_hash, tx_index, value):
                self.tx_hash = tx_hash
                self.tx_index = tx_index
                self.value = value

            def __repr__(self):
                return "<%s:%s with %s Satoshis>" % (
                    self.tx_hash,
                    self.tx_index,
                    self.value,
                )

        def get_utxos():
            utxos = []
            for f in self.listfunds().outputs:
                if f.status == "confirmed" and not f.reserved:
                    o = OutputInfo(tx_hash=f.txid, tx_index=f.output, value=f.value)
                    utxos.append(o)
            return utxos

        return select_outputs_greedy(unspent=get_utxos(), min_value=satoshis)
