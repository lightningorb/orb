# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-25 05:28:09
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-25 06:21:35


import uuid
import base64
import binascii

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import HMAC
from Crypto.PublicKey import RSA
from struct import pack


def generate_key(seed):
    class PRNG(object):
        def __init__(self, seed):
            self.index = 0
            self.seed = seed
            self.buffer = b""

        def __call__(self, n):
            while len(self.buffer) < n:
                self.buffer += HMAC.new(self.seed + pack("<I", self.index)).digest()
                self.index += 1
            result, self.buffer = self.buffer[:n], self.buffer[n:]
            return result

    return RSA.generate(
        2048,
        randfunc=PRNG(
            HMAC.new(bytes(seed, "utf-8") + b"Application: 2nd key derivation").digest()
        ),
    )


def encrypt(message, public_key, encoded=False):
    cipher = PKCS1_OAEP.new(RSA.importKey(public_key))
    if not encoded:
        message = str.encode(message)
    return base64.b64encode(cipher.encrypt(message))


def decrypt(encrypted_message, private_key):
    cipher = PKCS1_OAEP.new(RSA.importKey(private_key))
    try:
        return cipher.decrypt(base64.b64decode(encrypted_message))
    except binascii.Error:
        return None


def encrypt_long(message, private_key, encoded=False):
    ret = []
    for i in range(0, len(message), 100):
        ret.append(encrypt(message[i : i + 100], private_key, encoded).decode())
    return "\n".join(ret).encode()


def decrypt_long(encrypted_message, private_key):
    ret = []
    for l in encrypted_message.decode().split("\n"):
        ret.append(decrypt(l, private_key))
    return b"".join(ret)


def get_sec_keys(password=None):
    n = uuid.getnode()
    secret_key = generate_key(
        password
        or ":".join(
            ["{:02x}".format((n >> e) & 0xFF) for e in range(0, 8 * 6, 8)][::-1]
        )
        + ":orbpkpass1158eefa-aba0-477c-a2cd-9ad14d22c9cf"
    )
    return secret_key.exportKey("PEM"), secret_key.publickey().exportKey("PEM")


def get_cert_command(public_key):
    return f"""python3 -c 'from Crypto.Cipher import PKCS1_OAEP; from Crypto.PublicKey import RSA; import base64; import codecs; import os; cipher = PKCS1_OAEP.new(RSA.importKey("{public_key}")); print("\\n".join([base64.b64encode(cipher.encrypt(l.encode())).decode()for l in open(os.path.expanduser("~/.lnd/tls.cert")).read().split("\\n")]))'  """


def get_mac_command(public_key):
    return f"""python3 -c 'from Crypto.Cipher import PKCS1_OAEP; from Crypto.PublicKey import RSA; import base64; import codecs; import os; cipher = PKCS1_OAEP.new(RSA.importKey("{public_key}")); mac = open(os.path.expanduser("~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon"), "rb").read(); print("\\n".join([base64.b64encode(cipher.encrypt(mac[i : i + 100])).decode()for i in range(0, len(mac), 100)]))'  """
