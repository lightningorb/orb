# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-10 12:10:19
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-10 12:24:02

import base64
import rsa
import struct
import random
import sys

if (sys.version_info.major, sys.version_info.minor) < (3, 9):

    def randbytes(n):
        return random.getrandbits(n * 8).to_bytes(n, "little")

    random.randbytes = randbytes


def read_random_bits(nbits: int) -> bytes:
    """Monkeypatched so RSA uses the devices's MAC address
    and a key password for rand data generation, this makes
    the keys deterministic.

    Reads 'nbits' random bits.
    """
    nbytes, rbits = divmod(nbits, 8)
    randomdata = random.randbytes(nbytes)
    if rbits > 0:
        randomvalue = ord(random.randbytes(1))
        randomvalue >>= 8 - rbits
        randomdata = struct.pack("B", randomvalue) + randomdata
    return randomdata


rsa.randnum.read_random_bits = read_random_bits
