# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 06:45:34
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-03 16:29:39

import re
import os
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
from build_system import katching
from build_system import alembic
from build_system import cln_regtest


@task
def deploy_ios(c, bump: bool = False):
    if bump:
        versioning.bump_patch(c)
    ios.update(c)


@task
def release(c, minor=False, patch=False, hotfix=False):
    # if not hotfix or not "working tree clean" in c.run("git status").stdout:
    #     print("Working directory not clean")
    #     return
    rebase(push=False)
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
    rebase(push=True)


@task
def rebase(c, push=False):
    for branch in ["build_linux", "build_macosx", "build_windows", "docs", "site"]:
        c.run(f"git checkout {branch}")
        c.run("git rebase main")
        if push:
            c.run(f"git push --set-upstream origin {branch}")
    c.run("git checkout main")


namespace = Collection(
    lnd,
    cln,
    ssh,
    katching,
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
    rebase,
)
