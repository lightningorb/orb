# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:41:16
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-25 16:32:22

from invoke import task
import os


@task
def test(c):
    """
    Run the unit tests and doctests.
    """
    env = dict(
        PYTHONPATH=".:third_party:third_party/forex-python:third_party/currency-symbols"
    )
    c.run("python3.9 tests/test_sec_rsa.py", env=env)
    c.run("python3.9 tests/test_certificate.py", env=env)
    c.run("python3.9 tests/test_certificate_secure.py", env=env)
    c.run("python3.9 tests/test_macaroon_secure.py", env=env)
    c.run("python3.9 -m orb.math.Vector -v", env=env)
    c.run("python3.9 -m orb.math.lerp -v", env=env)
    c.run("python3.9 -m orb.misc.mempool -v", env=env)
    # c.run("python3.9 -m orb.misc.forex", env=env)
    c.run("python3.9 -m orb.misc.auto_obj -v", env=env)
