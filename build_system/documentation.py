# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:36:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 12:00:32

import os

from invoke import task


@task
def clean(c):
    """
    Delete the built docs. Useful when renaming modules etc.
    """
    c.run("rm -rf docs/docsbuild")


@task
def build(c, env=dict(PATH=os.environ["PATH"])):
    """
    Build the docs. Requires sphinx.
    """
    flags = (
        "--ext-autodoc --module-first --follow-links --ext-coverage --separate --force"
    )
    c.run(f"sphinx-apidoc {flags} -o docs/source/gen/ orb", env=env)
    c.run("sphinx-build -b html docs/source docs/docsbuild", env=env)


@task
def view(c):
    """
    View docs in the browser.
    """
    with c.cd("docs/docsbuild"):
        c.run("python3 -m http.server")
