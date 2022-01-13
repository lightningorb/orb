# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 06:45:34
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 09:09:29

import re
import os
from invoke import task, Context, Collection
import semver

get_ver = lambda: semver.VersionInfo.parse(open("VERSION").read().strip())
save_ver = lambda ver: open("VERSION", "w").write(str(ver))


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


@task()
def tag(c):
    ver = get_ver()
    print(ver)
    c.run(f'git tag -a v{ver} -m "tag v{ver}"')


@task
def push_tags(c):
    c.run("git push origin --tags")


@task()
def update_ios(c, env=dict(PATH=os.environ["PATH"])):
    path = "../lnorb-ios/lnorb.xcodeproj/project.pbxproj"
    content = open(path).read()
    ver = get_ver()

    c.run("make update_ios", env=env)

    content = re.sub(
        r"MARKETING_VERSION = \d+.\d+.\d+;",
        f"MARKETING_VERSION = {ver.major}.{ver.minor}.{ver.patch};",
        content,
    )

    open(path, "w").write(content)
