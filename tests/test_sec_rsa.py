# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-09 08:44:05
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-07 07:51:54

import unittest
from textwrap import dedent
from orb.misc.sec_rsa import *
from uuid import uuid4


class TestSec(unittest.TestCase):
    def test_key_gen(self):
        """
        Test that the keys are indeed deterministic
        """
        prev_priv, prev_pub = None, None
        for i in range(10):
            priv, pub = get_sec_keys()
            if prev_pub and prev_priv:
                self.assertEqual(pub, prev_pub)
                self.assertEqual(priv, prev_priv)
            prev_priv, prev_pub = priv, pub

    def test_encrypt_decrypt(self):
        """
        Test encrypting and decrypting a regular message using
        deterministic keys
        """
        priv, pub = get_sec_keys()
        msg = str.encode(str(uuid4()))
        secret = encrypt(msg, pub, True)
        plain = decrypt(secret, priv)
        self.assertEqual(msg, plain)

    def test_encrypt_decrypt_long(self):
        """
        Test encrypting and decrypting a long message using
        deterministic keys
        """
        priv, pub = get_sec_keys()
        msg = str.encode(str(uuid4()) * 1000)
        secret = encrypt_long(msg, pub, True)
        plain = decrypt_long(secret, priv)
        self.assertEqual(msg, plain)


if __name__ == "__main__":
    unittest.main()
