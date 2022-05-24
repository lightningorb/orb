# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:20:45
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-05-25 07:02:46


from fabric import Connection
import zipfile
from pathlib import Path
from invoke import task
import os


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), path),
            )


@task
def upload(c):
    """
    Upload site.
    """
    zipf = zipfile.ZipFile("site.zip", "w", zipfile.ZIP_DEFLATED)
    zipdir("site/public", zipf)
    zipf.close()
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        con.put("site.zip", "/home/ubuntu/lnorb_com/")
        with con.cd("/home/ubuntu/lnorb_com/"):
            con.run("rm -rf build css fonts images scss")
            con.run("unzip -o site.zip")


@task
def build(c, env=os.environ):
    with c.cd("site"):
        c.run("npm run build", env=env)


@task
def run(c, env=os.environ):
    with c.cd("site"):
        c.run("npm run dev", env=env)


@task
def spawn_mac_build(c):
    import rsa
    import uuid
    import codecs
    import base64
    import git
    import random

    print("The MAC address in formatted way is : ", end="")
    mac_address = "-".join(
        ["{:02x}".format((uuid.getnode() >> ele) & 0xFF) for ele in range(0, 8 * 6, 8)][
            ::-1
        ]
    )
    print(mac_address)
    pubkey = rsa.PublicKey.load_pkcs1(
        """-----BEGIN RSA PUBLIC KEY-----
MEgCQQCCIV6XxOjPkkW+0WJU+g64xbEYgOu3MZLyjmIJRJzbyEKi9jKukluu2TQ0
rb/kaSj3YCRjw4oQgr/YR3DShAJpAgMBAAE=
-----END RSA PUBLIC KEY-----"""
    )
    encrypted = rsa.encrypt(mac_address.encode(), pubkey)
    encoded = codecs.encode(encrypted, "hex").decode()
    repo = git.Repo(".")
    with open(".rand", "w") as f:
        f.write(str(random.random()))
    repo.index.add(".rand")
    repo.index.commit(encoded)
    origin = repo.remote(name="origin")
    origin.push()
