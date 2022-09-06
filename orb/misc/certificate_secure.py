# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-09 08:41:00
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-06 12:51:52

import codecs

from orb.misc.certificate import Certificate
from orb.misc.sec_rsa import *


class CertificateSecure:
    def __init__(self, cert_secure):
        self.cert_secure = cert_secure

    @staticmethod
    def init_from_encrypted(text):
        return CertificateSecure(text)

    @staticmethod
    def init_from_plain(text, uid=None):
        _, pub = get_sec_keys(uid=uid)
        encrypted = encrypt_long(str.encode(text), pub, True)
        return CertificateSecure(encrypted)

    @staticmethod
    def init_from_hex(cert_hex, uid=None):
        if type(cert_hex) is str:
            cert_hex = cert_hex.encode()
        text = codecs.decode(cert_hex, "hex")
        _, pub = get_sec_keys(uid=uid)
        encrypted = encrypt_long(text, pub, True)
        return CertificateSecure(encrypted)

    def as_plain_certificate(self):
        priv, _ = get_sec_keys()
        plain = decrypt_long(self.cert_secure, priv)
        return Certificate.init_from_str(plain.decode())
