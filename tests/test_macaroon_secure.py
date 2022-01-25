# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-09 08:44:05
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-25 17:47:45

import unittest
import codecs
from textwrap import dedent
from pathlib import Path

from orb.misc.sec_rsa import *
from orb.misc.macaroon_secure import MacaroonSecure

mac_bin_data = open(Path(__file__).parent / "readonly.macaroon", "rb").read()
mac_hex_data = codecs.encode(mac_bin_data, "hex")


class TestMacaroonSecure(unittest.TestCase):
    def test_init_from_plain(self):
        mac_secure = MacaroonSecure.init_from_plain(mac_hex_data)
        mac_plain = mac_secure.as_plain_macaroon()
        self.assertEqual(mac_hex_data, mac_plain.macaroon)

    def test_init_from_secure(self):
        mac_secure_from_plain = MacaroonSecure.init_from_plain(mac_hex_data)

        mac_secure = MacaroonSecure.init_from_encrypted(
            mac_secure_from_plain.macaroon_secure
        )
        mac_plain = mac_secure.as_plain_macaroon()
        self.assertEqual(mac_hex_data, mac_plain.macaroon)

    def test_is_well_formed(self):
        mac_secure = MacaroonSecure.init_from_plain(mac_hex_data)
        mac_plain = mac_secure.as_plain_macaroon()
        self.assertTrue(mac_plain.is_well_formed())


if __name__ == "__main__":
    unittest.main()
