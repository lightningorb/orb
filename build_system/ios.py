# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:00:02
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-03 09:19:29

import os
import re
import json
from glob import glob

from invoke import task
from build_system.semantic import *


def update_version(c):
    """
    Reflect the version change in xcode project.
    """
    path = "build/lnorb-ios/lnorb.xcodeproj/project.pbxproj"
    content = open(path).read()
    ver = get_ver()

    content = re.sub(
        r"MARKETING_VERSION = \d+.\d+.\d+;",
        f"MARKETING_VERSION = {ver.major}.{ver.minor}.{ver.patch};",
        content,
    )

    open(path, "w").write(content)


def copy_files(c):
    c.run("rm -rf /tmp/lnorb/")
    c.run("mkdir -p /tmp/lnorb/")
    c.run("cp -r VERSION third_party main.py images orb /tmp/lnorb/")


def copy_obfuscated_files(c):
    c.run("rm -rf /tmp/lnorb/")
    c.run("mkdir -p /tmp/lnorb/")
    c.run("cp -r images tmp/orb/* /tmp/lnorb/")


@task()
def update(c, env=dict(PATH=os.environ["PATH"])):
    """
    Update the xcode project with the latest changes.
    """
    update_version(c)
    copy_files(c)
    with c.cd("build"):
        c.run("toolchain update lnorb-ios", env=env)


# @task()
# def update(c, env=os.environ):
#     """
#     Try to deploy in obfuscated mode.
#     """
#     update_version(c)
#     c.run("rm -rf dist tmp;")
#     c.run("mkdir -p tmp;")
#     c.run("cp -r main.py tmp/;")
#     c.run("cp -r third_party tmp/;")
#     c.run("cp -r orb tmp/;")
#     with c.cd("tmp"):
#         c.run(
#             "pyarmor obfuscate --no-cross-protection --platform darwin.arm64.0 --recursive main.py;",
#             env=env,
#         )
#         c.run("cp -r orb/lnd/grpc_generated dist/orb/lnd/grpc_generated")
#         c.run("mkdir -p dist/orb/images")
#         c.run("cp -r orb/images/shadow_inverted.png dist/orb/images/")
#         c.run("cp -r orb/misc/settings.json dist/orb/misc/")
#         c.run("cp -r orb/apps/auto_fees/autofees.kv dist/orb/apps/auto_fees/")
#         c.run("cp -r orb/apps/auto_fees/autofees.png dist/orb/apps/auto_fees/")
#         c.run("cp -r orb/apps/auto_fees/appinfo.yaml dist/orb/apps/auto_fees/")
#         c.run(
#             "cp -r orb/apps/auto_rebalance/autobalance.kv dist/orb/apps/auto_rebalance/"
#         )
#         c.run(
#             "cp -r orb/apps/auto_rebalance/autobalance.png dist/orb/apps/auto_rebalance/"
#         )
#         c.run(
#             "cp -r orb/apps/auto_rebalance/appinfo.yaml dist/orb/apps/auto_rebalance/"
#         )
#         c.run(
#             "cp -r orb/apps/auto_max_htlcs/update_max_htlcs.png dist/orb/apps/auto_max_htlcs/"
#         )
#         c.run(
#             "cp -r orb/apps/auto_max_htlcs/appinfo.yaml dist/orb/apps/auto_max_htlcs/"
#         )
#         c.run("mkdir -p dist/images/")
#         c.run("cp -r ../images/ln.png dist/images/")
#         c.run("rm -rf orb main.py third_party")
#         c.run("mv dist orb")
#     copy_obfuscated_files(c)
#     with c.cd("build"):
#         out = c.run("security find-identity", env=env).stdout
#         identity = re.search(r'1\) ([A-Z 0-9]{40}) "Apple Development', out).group(1)
#         c.run("toolchain update lnorb-ios", env=env)
#         c.run(
#             f'codesign -f -s "{identity}" ./lnorb-ios/YourApp/pytransform/_pytransform.dylib',
#             env=env,
#         )
#         c.run(
#             f'codesign -f -s "{identity}" /tmp/lnorb/pytransform/_pytransform.dylib',
#             env=env,
#         )


@task
def create(c, env=dict(PATH=os.environ["PATH"])):
    """
    Create the xcode project.
    """
    copy_files(c)
    c.run("rm -rf build/lnorb-ios")
    with c.cd("build"):
        c.run("toolchain create lnorb /tmp/lnorb/", env=env)
    update_version(c)


@task
def toolchain_pip(c, env=dict(PATH=os.environ["PATH"])):
    with c.cd("build"):
        c.run("toolchain pip3 install kivymd==0.104.2", env=env)
        c.run("toolchain pip3 install peewee==3.14.8", env=env)
        c.run("toolchain pip3 install python-dateutil==2.8.2", env=env)
        c.run("toolchain pip3 install kivy_garden.graph==0.4.0", env=env)
        c.run("toolchain pip3 install PyYaml==6.0", env=env)
        c.run("toolchain pip3 install simplejson==3.17.6", env=env)
        # c.run("toolchain pip3 install pycryptodome", env=env)
        c.run("toolchain pip3 install memoization", env=env)
        c.run("toolchain pip3 install rsa", env=env)


@task
def toolchain_build(c, env=os.environ):
    with c.cd("build"):
        c.run("toolchain build python3", env=env)
        c.run("toolchain build openssl", env=env)
        c.run("toolchain build kivy", env=env)
        c.run("toolchain build pillow", env=env)
        c.run("toolchain build libzbar", env=env)
        c.run("toolchain build audiostream", env=env)
        c.run("toolchain build pyyaml", env=env)
        c.run("toolchain build plyer", env=env)
        c.run("toolchain build bcrypt", env=env)


@task
def tmp(c, env=os.environ):
    with c.cd("../kivy-ios-master"):
        c.run("python3.9 setup.py install --user", env=env)
    with c.cd("build"):
        c.run("toolchain build cryptography", env=env)


@task
def toolchain(c, env=dict(PATH=os.environ["PATH"]), clean=False):
    """
    Build and install all libs and modules required for XCode.
    """
    if clean:
        with c.cd("build"):
            c.run("toolchain distclean", env=env)
    toolchain_build(c, env)
    toolchain_pip(c, env)


@task
def clean(c, env=dict(PATH=os.environ["PATH"]), clean=False):
    """
    Clean all XCode libs and modules
    """
    with c.cd("build"):
        c.run("toolchain distclean", env=env)
