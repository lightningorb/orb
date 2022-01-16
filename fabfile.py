# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 06:45:34
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-16 08:15:21

import re
import os
from invoke import task, Context, Collection
from build_system.monkey_patch import fix_annotations

fix_annotations()

from build_system import third_party
from build_system import versioning
from build_system import ios
from build_system import tags
from build_system import submodules
from build_system import documentation
from build_system import test
from build_system import release_notes


@task
def deploy_ios(c, bump: bool = False):
    if bump:
        versioning.bump_patch(c)
    release_notes.create(c)
    ios.update(c)


namespace = Collection(
    deploy_ios,
    third_party,
    versioning,
    ios,
    submodules,
    documentation,
    test,
    release_notes,
    tags,
)
