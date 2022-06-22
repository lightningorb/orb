# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-22 07:58:03
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-22 09:13:39

from invoke import task
from pathlib import Path
from fabric import Connection
import os


@task
def start(c, env=os.environ):
    with c.cd("lnappstore"):
        c.run(f"npm run dev", env=env)


@task
def deploy(c, env=os.environ):
    c.run(
        "zip -r lnappstore lnappstore -x -x lnappstore/node_modules/**\* -x lnappstore/__sapper__/**\*",
        env=env,
    )
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as c:
        c.run("rm -rf /home/ubuntu/lnappstore_com/")
        c.run("mkdir -p /home/ubuntu/lnappstore_com/")
        c.put("lnappstore.zip", "/home/ubuntu/lnappstore_com/")
        with c.cd("/home/ubuntu/lnappstore_com/"):
            c.run("unzip lnappstore.zip")
        with c.cd("/home/ubuntu/lnappstore_com/lnappstore"):
            c.run("npm install")
