# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:41:16
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-23 07:28:33

from invoke import task
import os
from textwrap import dedent

os.environ["KIVY_NO_ARGS"] = "1"


@task
def test(c, cython=False):
    """
    Run the unit tests and doctests.
    """
    env = os.environ
    if cython:
        c.run(f"python3 build_system/setup.py build_ext --inplace", env=env)
    else:
        c.run('rm -f `find . -name "*.so"`')
    c.run("rm -rf coverage")
    c.run(
        "source third_party/load_env.sh && env ORB_INTEGRATION_TESTS=1 nosetests --nologcapture --with-coverage --cover-inclusive --cover-html --cover-html-dir=coverage --cover-erase --cover-package orb --with-doctest tests/",
        env=env,
    )
