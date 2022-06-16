# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-08 10:18:11
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-08 10:42:39

import unittest
import passlib


class TestBCrypt(unittest.TestCase):
    def test_bcrypt(self):
        import bcrypt

        passwd = b"s$cret12"
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwd, salt)
        self.assertTrue(bcrypt.checkpw(passwd, hashed))

    def test_bcrypt_kdf(self):
        from cryptography.hazmat.primitives.ciphers import algorithms
        from twisted.python import randbytes
        import bcrypt

        cipher = algorithms.AES
        blockSize = cipher.block_size // 8
        ivSize = blockSize
        keySize = 32
        salt = randbytes.secureRandom(ivSize)
        r = bcrypt.kdf(b"test", salt, keySize + ivSize, 100)
        self.assertTrue(r)

    def test_passlib(self):
        from passlib.hash import bcrypt

        passwd = b"s$cret12"
        hashed = bcrypt.hash(passwd)

        self.assertTrue(bcrypt.verify(passwd, hashed))


if __name__ == "__main__":
    unittest.main()
