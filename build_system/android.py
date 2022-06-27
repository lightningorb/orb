# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-26 10:22:54
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-26 18:41:44

from fabric import Connection
from invoke import task
from pathlib import Path
import os


@task
def install(c, env=os.environ):
    c.run(f"pip3 install python-for-android", env=env)


@task
def build(c, env=os.environ):
    c.run(
        "rm -f ~/orb/bin/orb-0.1-arm64-v8a_armeabi-v7a-debug.apk ~/lnorb_com/orb-0.1-arm64-v8a_armeabi-v7a-debug.apk"
    )
    env[
        "PATH"
    ] = "/home/ubuntu/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
    c.run(f"buildozer android debug", env=env)
    c.run("cp -f ~/orb/bin/orb-0.1-arm64-v8a_armeabi-v7a-debug.apk ~/lnorb_com/")


@task
def build_remote(c, env=os.environ):
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        with con.cd("orb"):
            con.run("./build.py android.build")


@task
def sync(c, env=os.environ):
    c.run(
        "rsync -azv -e 'ssh -i lnorb_com.cer' . ubuntu@lnorb.com:/home/ubuntu/orb/ --exclude build --exclude dist --exclude .cache --exclude lnappstore/node_modules --exclude site/node_modules",
        env=env,
    )
