# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:00:02
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-17 08:31:58

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
    c.run(
        "cp -r third_party main.py images/ln.png images docs/docsbuild orb user video_library.yaml fees.yaml autobalance.yaml images/orb.png user_scripts.json /tmp/lnorb/"
    )


def get_auto_balance():
    return """
#rules:
#- !Ignore
#  alias: LOOP
#  any:
#  - channel.remote_pubkey == '021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'
#- !To
#  alias: SeasickDiver
#  fee_rate: 800
#  num_sats: 10_000
#  all:
#  - channel.remote_pubkey == '021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'
#  - channel.local_balance / channel.capacity < 0.5
#- !To
#  alias: bfx-lnd0
#  num_sats: 100_000
#  fee_rate: 400
#  all:
#  - channel.remote_pubkey == '033d8656219478701227199cbd6f670335c8d408a92ae88b962c49d4dc0e83e025'
#  - channel.local_balance / channel.capacity < 0.5"""


def prep_user_scripts(c):
    def comment_out(content):
        return "\n".join(f"# {l}" for l in content.split("\n"))

    user_scripts = {}
    for g in ["user/scripts/*.py", "fees.yaml"]:
        for f in glob(g):
            content = open(f).read()
            user_scripts[f] = comment_out(content) if ".yaml" in g else content

    user_scripts["autobalance.yaml"] = get_auto_balance()

    with open("user_scripts.json", "w") as f:
        f.write(json.dumps(user_scripts, indent=4))

    print("user_scripts.json should be good")


@task()
def update(c, env=dict(PATH=os.environ["PATH"])):
    """
    Update the xcode project with the latest changes.
    """
    update_version(c)
    prep_user_scripts(c)
    copy_files(c)
    with c.cd("build"):
        c.run("toolchain update lnorb-ios", env=env)


@task
def create(c, env=dict(PATH=os.environ["PATH"])):
    """
    Create the xcode project.
    """
    prep_user_scripts(c)
    copy_files(c)
    c.run("rm -rf build/lnorb-ios")
    with c.cd("build"):
        c.run("toolchain create lnorb /tmp/lnorb/", env=env)
    update_version(c)
