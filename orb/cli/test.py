# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-27 06:44:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-09 09:40:52

from invoke import task

import typer

app = typer.Typer()


@app.command()
def run_all_tests():
    """
    Run all tests. This does not include doctests.

    .. asciinema:: /_static/orb-test-run-all-tests.cast
    """
    import os
    import pytest

    os.environ["ORB_INTEGRATION_TESTS"] = "1"
    # pytest.main(["--doctest-modules", "orb/math", "orb/misc", "tests"])
    pytest.main(["tests", "--disable-warnings"])
