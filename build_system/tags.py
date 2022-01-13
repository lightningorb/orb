# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 10:58:57
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 11:02:33

from build_system.semantic import *


@task()
def tag(c):
    ver = get_ver()
    print(ver)
    c.run(f'git tag -a v{ver} -m "tag v{ver}"')


@task
def push(c):
    c.run("git push origin --tags")
