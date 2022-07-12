import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(
    BLOCK_SIZE - len(s) % BLOCK_SIZE
)
unpad = lambda s: s[: -ord(s[len(s) - 1 :])]

password = "asdf"


def r_pad(payload, block_size=16):
    length = block_size - (len(payload) % block_size)
    return payload + chr(length).encode() * length


def encrypt(raw):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = raw.encode()
    raw = r_pad(raw)
    assert len(raw) % 16 == 0
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    decoded = bytes.decode(unpad(cipher.decrypt(enc[16:])))
    return compile(decoded, "<string>", "exec")


# with open("orb/core/logging.py") as f:
#     enc = encrypt(f.read())
#     decrypt(enc)
