# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:20:45
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-05-25 07:02:46

from fabric import Connection
from invoke import task
import os


@task
def build(c, env=os.environ):
    """
    Build the website using npm.

    Parameters:
        c (Connection): The Fabric connection object.
        env (os._Environ): The environment variables. Defaults to `os.environ`.
    """
    with c.cd("site"):
        c.run("npm run build", env=env)


@task
def run(c, env=os.environ):
    """
    Run the website using npm in development mode.

    Parameters:
        c (Connection): The Fabric connection object.
        env (os._Environ): The environment variables. Defaults to `os.environ`.
    """
    with c.cd("site"):
        c.run("npm run dev", env=env)
