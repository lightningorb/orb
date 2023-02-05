# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-09-25 11:25:52
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-28 12:23:55

import os
from pathlib import Path
from textwrap import dedent
from fabric import Connection
from invoke import task, Responder


@task
def orb_vnc(c):
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    VERSION = open("VERSION").read().strip()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        con.run("mkdir -p /tmp/asdf")
        with con.cd("/tmp/asdf"):
            con.put("images/orb-256x256.png", "/tmp/asdf/orb-256x256.png")
            con.put("images/orb-128x128.png", "/tmp/asdf/orb-128x128.png")
            con.put("images/orb-48x48.png", "/tmp/asdf/orb-48x48.png")
            con.put("images/orb-32x32.png", "/tmp/asdf/orb-32x32.png")
            con.put("images/orb-16x16.png", "/tmp/asdf/orb-16x16.png")
            con.put("images/orb-16x16.png", "/tmp/asdf/orb-16x16.png")
            con.put("build_system/pcmanfm.conf", "/tmp/asdf/pcmanfm.conf")
            con.put("build_system/orb.desktop", "/tmp/asdf/orb.desktop")
            con.put("build_system/dockerfile.vnc", "/tmp/asdf/dockerfile.vnc")
            con.put("build_system/startup.sh", "/tmp/asdf/startup.sh")
            con.put("images/bg.jpeg", "/tmp/asdf/bg.jpeg")
            con.run(f"docker build -t lnorb/orb-vnc:{VERSION} -f dockerfile.vnc .")
            con.run(f"docker tag lnorb/orb-vnc:{VERSION} lnorb/orb-vnc:latest")
            con.run("docker push lnorb/orb-vnc:latest")
