# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:20:45
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-02 09:26:00


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
            con.run("unzip -o site.zip")


@task
def build(c, env=os.environ):
    with c.cd("site"):
        c.run("npm run build", env=env)
