# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-11 09:24:29

import codecs
import re
from typing import Union


class LndBase:
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
