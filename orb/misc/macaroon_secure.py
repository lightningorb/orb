# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-09 08:41:00
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-06 12:34:37

from orb.misc.macaroon import Macaroon
from orb.misc.sec_rsa import *


class MacaroonSecure:
    def __init__(self, macaroon_secure):
        self.macaroon_secure = macaroon_secure

    @staticmethod
    def init_from_encrypted(text):
        return MacaroonSecure(text)

    @staticmethod
    def init_from_plain(bin_data, uid=None):
        """
        This is super confusing. Is it plain or hex? Clearly hex
        so ought to be renamed.
        """
        if type(bin_data) is str:
            bin_data = bin_data.encode()
        _, pub = get_sec_keys(uid=uid)
        encrypted = encrypt_long(bin_data, pub, True)
        return MacaroonSecure(encrypted)

    def as_plain_macaroon(self):
        """
        Plain or hex?
        """
        priv, _ = get_sec_keys()
        plain = decrypt_long(self.macaroon_secure, priv)
        return Macaroon.init_from_not_sure(plain)
