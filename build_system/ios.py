# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:00:02
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 15:45:47

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
        "cp -r main.py images/ln.png images docs/docsbuild orb user video_library.yaml fees.yaml autobalance.yaml images/orb.png user_scripts.json /tmp/lnorb/"
    )


def prep_user_scripts(c):
    def comment_out(content):
        return "\n".join(f"# {l}" for l in content.split("\n"))

    user_scripts = {}
    for g in ["user/scripts/*.py", "fees.yaml", "autobalance.yaml"]:
        for f in glob(g):
            content = open(f).read()
            user_scripts[f] = comment_out(content) if ".yaml" in g else content

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
