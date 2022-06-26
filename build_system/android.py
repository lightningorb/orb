# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-26 10:22:54
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-26 18:00:48

from invoke import task
import os


@task
def install(c, env=os.environ):
    c.run(f"pip3 install python-for-android", env=env)


@task
def build(c, env=os.environ):
    c.run(f"buildozer android debug", env=env)
