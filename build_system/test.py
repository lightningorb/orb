# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:41:16
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-27 12:37:24

from invoke import task
import os
from textwrap import dedent

os.environ["KIVY_NO_ARGS"] = "1"


@task
def test(c, cython=False):
    """
    Run the unit tests and doctests.
    """
    import pytest

    env = os.environ
    if cython:
        c.run(f"python3 build_system/setup.py build_ext --inplace", env=env)
    else:
        c.run('rm -f `find . -name "*.so"`')

    pytest.main(["--doctest-modules", "orb/math", "orb/misc", "tests"])
