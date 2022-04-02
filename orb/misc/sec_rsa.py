# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-25 05:28:09
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-04-02 10:18:49


import uuid
import base64
import binascii
import rsa
import struct
import os
import random
from traceback import format_exc
from orb.misc.utils import pref
from orb.misc.utils import desktop
import plyer
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


def get_sec_keys():
    if pref("system.identifier") == "uuid":
        uid = uuid.getnode()
    elif pref("system.identifier") == "plyer":
        uid = plyer.uniqueid.id
    random.seed(f"{uid}-orbkeygenpass-3802f003-bc64-47e3-a64f-82f57945271b")
    (pub, priv) = rsa.newkeys(nbits=512, accurate=True)
    return priv.save_pkcs1(), pub.save_pkcs1()


def get_cert_command(public_key):
    cert_path = "~/.lnd/tls.cert"
    if pref("lnd.type") == "umbrel":
        cert_path = "~/umbrel/lnd/tls.cert"
    return f"""python3 -c "import rsa; import base64; import os; p = rsa.PublicKey.load_pkcs1({public_key}); c = open(os.path.expanduser('{cert_path}')).read(); print('\\n'.join([base64.b64encode(rsa.encrypt(c[i : i + 53].encode(), p)).decode() for i in range(0, len(c), 53)]))"  """


def get_mac_command(public_key):
    mac_path = "~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon"
    if pref("lnd.type") == "umbrel":
        mac_path = "~/umbrel/lnd/data/chain/bitcoin/mainnet/admin.macaroon"
    return f"""python3 -c "import rsa; import os; import codecs; import base64; pub = rsa.PublicKey.load_pkcs1({public_key}); message = codecs.encode(open(os.path.expanduser('{mac_path}'), 'rb' ).read(), 'hex',).decode(); print('\\n'.join([base64.b64encode(rsa.encrypt(message[i : i + 53].encode('utf8'), pub)).decode() for i in range(0, len(message), 53)]))"  """
