# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 06:45:34
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-01 21:21:00

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
from build_system import submodules
from build_system import documentation
from build_system import test
from build_system import release_notes
from build_system import appstore
from build_system import host
from build_system import armor
from build_system import site


@task
def deploy_ios(c, bump: bool = False):
    if bump:
        versioning.bump_patch(c)
    documentation.build(c)
    release_notes.create(c)
    ios.update(c)


namespace = Collection(
    deploy_ios,
    third_party,
    versioning,
    ios,
    osx,
    submodules,
    documentation,
    test,
    release_notes,
    tags,
    appstore,
    host,
    ubuntu,
    armor,
    site,
)
