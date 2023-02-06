# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 06:45:34
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-27 11:09:53

import re
import os
from pathlib import Path
from invoke import task, Context, Collection
from build_system.monkey_patch import fix_annotations

fix_annotations()

from build_system import lnd
from build_system import cln
from build_system import ssh
from build_system import android
from build_system import ios
from build_system import osx
from build_system import ubuntu
from build_system import third_party
from build_system import versioning
from build_system import tags
from build_system import documentation
from build_system import test
from build_system import appstore
from build_system import host
from build_system import armor
from build_system import site
from build_system import alembic
from build_system import cln_regtest
from build_system import docker


@task
def deploy_ios(c, bump: bool = False):
    if bump:
        versioning.bump_patch(c)
    ios.update(c)


@task
def release(c, minor=False, patch=False, hotfix=False):
    merge(c, push=False)
    if not hotfix:
        if minor and patch:
            exit(-1)
        if not (minor or patch):
            print("Need either minor or patch")
            exit(-1)
        if patch:
            versioning.bump_patch(c)
        if minor:
            versioning.bump_minor(c)
    if hotfix:
        c.run("git commit -am 'release hotfix'", warn=True)
    else:
        c.run("git commit -am 'version bump'")
    c.run("git push --set-upstream origin main")
    if not hotfix:
        tags.tag(c)
        tags.push(c)
    merge(c, push=True)
    update_install_script(c)


@task
def update_install_script(c):
    from fabric import Connection

    with open("VERSION") as f:
        VERSION = f.read()
    with open("install.sh") as f:
        installsh = f.read().replace("<VERSION>", VERSION)
        with open("/tmp/install.sh", "w") as w:
            w.write(installsh)
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        con.put("/tmp/install.sh", "/home/ubuntu/install_orb/index.html")


@task
def merge(c, push=False):
    for branch in [
        "build_linux",
        "build_docker",
        "build_macosx",
        "build_windows",
        "build_android",
        "build_vnc",
        "docs",
        "site",
    ]:
        c.run(f"git checkout {branch}")
        c.run("git pull")
        c.run("git merge main -m 'merging changes from main'")
        if push:
            c.run(f"git push --set-upstream origin {branch}")
    c.run("git checkout main")


namespace = Collection(
    lnd,
    cln,
    ssh,
    release,
    deploy_ios,
    third_party,
    versioning,
    ios,
    osx,
    documentation,
    test,
    tags,
    appstore,
    host,
    ubuntu,
    armor,
    site,
    alembic,
    android,
    cln_regtest,
    merge,
    update_install_script,
    docker,
)
