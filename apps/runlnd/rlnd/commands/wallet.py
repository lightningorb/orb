import re
import os
import quantumrandom
import pyzipper
from getpass import getpass
from invoke import task
from invoke import Responder

from .prefs import get_secrets_path
from .prefs import get_key_path


def save_secrets(entropy, mnemonic, zip_file_name):
    print(f"Saving your wallet's seed and entropy to {zip_file_name}")
    wallet_pw = os.environ.get("wallet_password", None)
    with pyzipper.AESZipFile(
        zip_file_name, "w", compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES
    ) as zf:
        while True:
            pw1_first = wallet_pw or getpass("   Type in password for zip secrets: ")
            pw2_first = wallet_pw or getpass("Re-Type in password for zip secrets: ")
            if pw1_first != pw2_first:
                print("Mismatch!")
            else:
                zf.setpassword(pw1_first.encode())
                zf.writestr("mnemonic.txt", mnemonic)
                zf.writestr("entropy.txt", entropy)
                break
    os.chmod(zip_file_name, 0o400)


def read_secrets(zip_file_name):
    print("Reading secrets", zip_file_name)
    wallet_pw = os.environ.get("wallet_password", None)
    with pyzipper.AESZipFile(zip_file_name) as zf:
        while True:
            pw = wallet_pw or getpass("   Type in password for zip secrets: ")
            zf.setpassword(pw.encode())
            try:
                return (
                    zf.read("entropy.txt").decode("utf-8"),
                    zf.read("mnemonic.txt").decode("utf-8"),
                )
            except:
                print("Wrong password!")


@task
def create(c, node_name):
    """
    Create lnd wallet. This includes using cryptographically
    secure entropy from QRNG (https://qrng.anu.edu.au/).
    Save wallet information into a password protected zip file
    in ~/.rln/secrets.zip.

    If the secrets.zip file exists, then it's used to restore
    the wallet information on the node.

    https://github.com/lightningnetwork/lnd/blob/master/docs/recovery.md#24-word-cipher-seeds
    """
    zip_file_name = get_secrets_path(node_name)
    entropy, mnemonic = (
        read_secrets(zip_file_name)
        if os.path.exists(zip_file_name)
        else (quantumrandom.hex()[:32], None)
    )
    c.run(f"echo '{entropy}' > ~/.lnd/wallet_password")
    responders = [
        Responder(
            pattern=r"Input wallet password:",
            response=entropy + "\n",
        ),
        Responder(
            pattern=r"Confirm password:",
            response=entropy + "\n",
        ),
        Responder(
            pattern="Do you have an existing cipher seed mnemonic you want to use\? \(Enter y/n\):",
            response="yn"[mnemonic is None] + "\n",
        ),
        Responder(
            pattern=r"Input your 24-word mnemonic separated by spaces:",
            response=(mnemonic or "") + "\n",
        ),
        Responder(
            pattern=r"Input an optional address look-ahead used to scan for used keys \(default 2500\):",
            response="\n",
        ),
        Responder(
            pattern="Input your cipher seed passphrase \(press enter if your seed doesn't have a passphrase\):",
            response="\n",
        ),
        Responder(
            pattern=r".*Input your passphrase if you wish to encrypt it \(or press enter to proceed without a cipher seed passphrase\):",
            response="\n",
        ),
    ]
    out = c.run(f"lncli create", pty=True, watchers=responders).stdout
    out = out.split("BEGIN LND CIPHER SEED")[1].split("END LND CIPHER SEED")[0]
    mnemonic_gen = " ".join(
        m.groups()[0] for m in re.finditer(r"\d+\. (\w+)", out, re.MULTILINE)
    )
    if mnemonic:
        assert mnemonic_gen == mnemonic
    else:
        save_secrets(entropy, mnemonic_gen, zip_file_name)
