# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:07:42
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 11:12:53

from invoke import task


@task
def remove_all(c):
    """
    Delete the relevant section from the .gitmodules file.
    Stage the .gitmodules changes:
    git add .gitmodules
    Delete the relevant section from .git/config.
    Remove the submodule files from the working tree and index:
    git rm --cached path_to_submodule (no trailing slash).
    Remove the submodule's .git directory:
    rm -rf .git/modules/path_to_submodule
    Commit the changes:
    git commit -m "Removed submodule <name>"
    Delete the now untracked submodule files:
    rm -rf path_to_submodule
    """
    c.run("rm -f .gitmodules")
    c.run("rm -rf .git/modules/*")
    c.run("git rm .gitmodules")
    c.run("git rm --cached third_party/arrow")
