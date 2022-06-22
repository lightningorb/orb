# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-18 17:03:03
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-08 05:33:50

from invoke import task
import os

# ./build.py -H ubuntu@18.118.53.220 -i orbdb.cer app-store.provision


@task
def start(c, env=os.environ):
    env["PYTHONPATH"] = "../"
    uvcpath = "/Library/Frameworks/Python.framework/Versions/3.7/bin/uvicorn"
    with c.cd("server"):
        c.run(f"{uvcpath} orb_server:app --reload", env=env)


@task
def create_db(c, env=os.environ):
    with c.cd("server"):
        c.run(
            "/Library/Frameworks/Python.framework/Versions/3.9/bin/python3 create_db.py"
        )


@task
def start_katching_service(c, env=os.environ):
    with c.cd("server"):
        c.run(
            "nameko run workers.katching_service --config workers/nameko-dev.yaml",
            env=env,
        )
