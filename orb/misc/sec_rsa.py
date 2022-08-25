# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-25 05:28:09
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-07 07:53:26


import base64
import random

import rsa

from orb.misc import patch_rand_bits
from orb.misc.device_id import device_id

keep = lambda _: _
keep(patch_rand_bits)


def encrypt(message, public_key, encoded=False):
    pub = rsa.PublicKey.load_pkcs1(public_key)
    if not encoded:
        message = str.encode(message)
    return base64.b64encode(rsa.encrypt(message, pub))


def decrypt(encrypted_message, private_key):
    priv = rsa.PrivateKey.load_pkcs1(private_key)
    try:
        return rsa.decrypt(base64.b64decode(encrypted_message), priv)
    except:
        # print(format_exc())
        # print(encrypted_message)
        # print("decryption failed")
        return b""


def encrypt_long(message, private_key, encoded=False):
    ret = []
    for i in range(0, len(message), 53):
        ret.append(encrypt(message[i : i + 53], private_key, encoded).decode())
    return "\n".join(ret).encode()


def decrypt_long(encrypted_message, private_key):
    ret = []
    for l in encrypted_message.decode().split("\n"):
        ret.append(decrypt(l, private_key))
    return b"".join(ret)


def get_sec_keys(uid=None):
    if uid is None:
        uid = device_id()
    random.seed(f"{uid}-orbkeygenpass-3802f003-bc64-47e3-a64f-82f57945271b")
    (pub, priv) = rsa.newkeys(nbits=512, accurate=True)
    return priv.save_pkcs1(), pub.save_pkcs1()
