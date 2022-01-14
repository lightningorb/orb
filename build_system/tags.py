# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 10:58:57
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-14 22:35:35

from build_system.semantic import *
from invoke import task


@task
def tag(c):
    ver = get_ver()
    print(ver)
    c.run(f'git tag -a v{ver} -m "tag v{ver}"')


@task
def push(c):
    c.run("git push origin --tags")
