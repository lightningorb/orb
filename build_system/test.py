# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:41:16
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-17 07:53:28

from invoke import task
import os

os.environ["KIVY_NO_ARGS"] = "1"


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
    # c.run("python3 tests/test_sec_rsa.py", env=env)
    # c.run("python3 tests/test_certificate.py", env=env)
    # c.run("python3 tests/test_certificate_secure.py", env=env)
    # c.run("python3 tests/test_macaroon_secure.py", env=env)
    # c.run("python3 -m orb.math.Vector -v", env=env)
    # c.run("python3 -m orb.math.lerp -v", env=env)
    # c.run("python3 -m orb.misc.mempool -v", env=env)
    # c.run("python3 -m orb.misc.auto_obj -v", env=env)
    # c.run("python -m orb.misc.forex", env=env)
