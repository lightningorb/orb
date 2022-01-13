# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 10:55:40
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 15:18:09

import os
from invoke import task


@task
def clone(c):
    """
    Stub.
    """
    if not os.path.exists("third_party/arrow"):
        c.run(
            "git submodule add https://github.com/arrow-py/arrow.git third_party/arrow/"
        )
        with c.cd("third_party/arrow"):
            c.run("git checkout 1.2.1")


@task
def clean(c):
    """
    Stub.
    """
    c.run("rm -rf third_party")
