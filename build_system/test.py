# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:41:16
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 11:41:40

from invoke import task


@task
def test(c):
    c.run("PYTHONPATH=. python3 tests/test_certificate.py")
    c.run("python3 -m orb.math.Vector -v")
    c.run("python3 -m orb.math.lerp -v")
    c.run("python3 -m orb.misc.mempool -v")
    c.run("python3 -m orb.misc.forex")
    c.run("python3 -m orb.misc.auto_obj -v")
