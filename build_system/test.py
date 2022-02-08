# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:41:16
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-09 07:23:03

from invoke import task
import os


@task
def test(c):
    """
    Run the unit tests and doctests.
    """
    env = os.environ
    with open(os.path.expanduser("~/nose.cfg"), "w") as f:
        f.write(
            """[nosetests]
verbosity=3
with-doctest=1"""
        )
    env.update(
        dict(
            PYTHONPATH=".:third_party:third_party/forex-python:third_party/currency-symbols"
        )
    )
    c.run("python3 -m 'nose'", env=env)
