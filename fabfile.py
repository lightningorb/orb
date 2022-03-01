# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 06:45:34
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-03-02 04:14:33

import re
import os
from invoke import task, Context, Collection
from build_system.monkey_patch import fix_annotations

fix_annotations()

from build_system import ios
from build_system import osx
from build_system import ubuntu
from build_system import third_party
from build_system import versioning
from build_system import tags
from build_system import documentation
from build_system import test
from build_system import release_notes
from build_system import appstore
from build_system import host
from build_system import armor
from build_system import site
from build_system import katching
from build_system import alembic


@task
def deploy_ios(c, bump: bool = False):
    if bump:
        versioning.bump_patch(c)
    release_notes.create(c)
    ios.update(c)


@task
def release(c, minor=False, patch=False):
    if not "working tree clean" in c.run("git status").stdout:
        print("Working directory not clean")
        return
    if minor and patch:
        exit(-1)
    if not (minor or patch):
        print("Need either minor or patch")
        exit(-1)
    release_notes.create(c)
    if patch:
        versioning.bump_patch(c)
    if minor:
        versioning.bump_minor(c)
    c.run("git commit -am 'version bump'")
    c.run("git push")
    tags.tag(c)
    tags.push()


namespace = Collection(
    katching,
    release,
    deploy_ios,
    third_party,
    versioning,
    ios,
    osx,
    documentation,
    test,
    release_notes,
    tags,
    appstore,
    host,
    ubuntu,
    armor,
    site,
    alembic,
)
