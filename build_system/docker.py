# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-09-25 11:25:52
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-25 11:50:39

import os
from pathlib import Path
from fabric import Connection
from invoke import task, Responder


@task
def orb_vcn(c):
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        con.run("mkdir -p /tmp/asdf")
        with con.cd("/tmp/asdf"):
            con.put("build_system/dockerfile.vnc", "/tmp/asdf/dockerfile.vnc")
            con.run("docker build -t lnorb/orb_vnc -f dockerfile.vnc .")
            con.run(
                "docker run -p 6080:80 -e USER=ubuntu --rm -v /dev/shm:/dev/shm lnorb/orb_vnc"
            )
