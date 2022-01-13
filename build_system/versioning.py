# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 10:57:41
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 11:03:11

from invoke import task
from build_system.semantic import *


@task()
def bump_build(c):
    ver = get_ver().bump_build()
    print(ver)
    save_ver(ver)


@task()
def bump_minor(c):
    ver = get_ver().bump_minor()
    print(ver)
    save_ver(ver)


@task()
def bump_major(c):
    ver = get_ver().bump_major()
    print(ver)
    save_ver(ver)


@task()
def bump_patch(c):
    ver = get_ver().bump_patch()
    print(ver)
    save_ver(ver)


@task()
def bump_pre(c):
    ver = get_ver().bump_prerelease()
    print(ver)
    save_ver(ver)
