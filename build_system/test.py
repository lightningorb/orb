# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:41:16
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-29 10:56:47

from invoke import task
import os


@task
def test(c):
    """
    Run the unit tests and doctests.
    """
    env = os.environ
    env.update(
        dict(
            PYTHONPATH=".:third_party:third_party/forex-python:third_party/currency-symbols"
        )
    )
    c.run("python tests/test_sec_rsa.py", env=env)
    c.run("python tests/test_certificate.py", env=env)
    c.run("python tests/test_certificate_secure.py", env=env)
    c.run("python tests/test_macaroon_secure.py", env=env)
    c.run("python -m orb.math.Vector -v", env=env)
    c.run("python -m orb.math.lerp -v", env=env)
    c.run("python -m orb.misc.mempool -v", env=env)
    # c.run("python -m orb.misc.forex", env=env)
    c.run("python -m orb.misc.auto_obj -v", env=env)
