# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 10:57:41
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 15:17:40

from invoke import task
from build_system.semantic import *


@task()
def bump_build(c):
    """
    Bump the build number using semver and store in VERSION.
    """
    ver = get_ver().bump_build()
    print(ver)
    save_ver(ver)


@task()
def bump_minor(c):
    """
    Bump the minor version using semver and store in VERSION.
    """
    ver = get_ver().bump_minor()
    print(ver)
    save_ver(ver)


@task()
def bump_major(c):
    """
    Bump the major version using semver and store in VERSION.
    """
    ver = get_ver().bump_major()
    print(ver)
    save_ver(ver)


@task()
def bump_patch(c):
    """
    Bump the patch version using semver and store in VERSION.
    """
    ver = get_ver().bump_patch()
    print(ver)
    save_ver(ver)


@task()
def bump_pre(c):
    """
    Bump the pre-release using semver and store in VERSION.
    """
    ver = get_ver().bump_prerelease()
    print(ver)
    save_ver(ver)
