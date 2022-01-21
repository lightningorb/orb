# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-18 17:03:03
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-20 08:45:23

from invoke import task
import os

# ./build.py -H ubuntu@18.118.53.220 -i orbdb.cer app-store.provision


@task
def start(c, env=os.environ["PATH"]):
    uvcpath = "/Library/Frameworks/Python.framework/Versions/3.9/bin/uvicorn"
    with c.cd("server"):
        c.run(f"{uvcpath} orb_server:app --reload")


@task
def create_db(c, env=os.environ["PATH"]):
    with c.cd("server"):
        c.run(
            "/Library/Frameworks/Python.framework/Versions/3.9/bin/python3 create_db.py"
        )
