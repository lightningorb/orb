# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-27 06:44:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-28 12:22:33

from invoke import task

import typer

app = typer.Typer()


@app.command()
def run_all_tests():
    """
    Run all tests.
    """
    import os
    import pytest

    os.environ["ORB_INTEGRATION_TESTS"] = "1"
    # pytest.main(["--doctest-modules", "orb/math", "orb/misc", "tests"])
    pytest.main(["tests"])
