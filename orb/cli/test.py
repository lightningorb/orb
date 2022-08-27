# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-27 06:44:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-27 12:37:41

from invoke import task


@task
def run_all_tests(c):
    """
    Run all tests.
    """
    import os
    import pytest

    os.environ["ORB_INTEGRATION_TESTS"] = "1"
    pytest.main(["--doctest-modules", "orb/math", "orb/misc", "tests"])
