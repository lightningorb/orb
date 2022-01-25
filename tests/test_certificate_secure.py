# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-09 08:44:05
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-25 17:44:54

import unittest
from textwrap import dedent
from orb.misc.sec_rsa import *
from orb.misc.certificate_secure import CertificateSecure
from uuid import uuid4


text = """\
-----BEGIN CERTIFICATE-----
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
bmQgYXV0b2dlbmVyYXRlZCBjZXJ0MRIwEAYDVQQDEwlsb2NhbGhvc3QwWTATBgcq
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAA
-----END CERTIFICATE-----"""


class TestCertificateSecure(unittest.TestCase):
    def test_init_from_plain(self):
        # init secure certificate from plain text string
        cert_secure = CertificateSecure.init_from_plain(text)
        # decrypt secure certificate to plain certificate
        cert = cert_secure.as_plain_certificate()
        self.assertEqual(cert.cert, text)
        self.assertEqual(
            cert.debug(),
            "Certificate correctly formatted",
        )
        self.assertEqual(text, cert.reformat())

    def test_init_from_secure(self):
        cert_secure_from_plain = CertificateSecure.init_from_plain(text)
        # init secure certificate from plain text string
        cert_secure = CertificateSecure.init_from_encrypted(
            cert_secure_from_plain.cert_secure
        )
        # decrypt secure certificate to plain certificate
        cert = cert_secure.as_plain_certificate()
        self.assertEqual(cert.cert, text)
        self.assertEqual(
            cert.debug(),
            "Certificate correctly formatted",
        )
        self.assertEqual(text, cert.reformat())


if __name__ == "__main__":
    unittest.main()
