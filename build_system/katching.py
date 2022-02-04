# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-05 05:46:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-05 06:04:09

"""
Everything related to recieving and processing licence payments on
the LND node.
"""

from invoke import task


@task
def deploy_katching(c):
    with c.cd("orb"):
        c.run("git stash")
        c.run("git pull")
        c.put("build_system/katching.conf", "/tmp/")
    c.sudo("mv /tmp/orb.conf /etc/supervisor/conf.d/")
    c.sudo("supervisorctl update")
