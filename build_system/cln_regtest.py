# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-09 13:08:51
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-09 15:12:13

import os
from invoke import task


@task
def setup(c, env=os.environ):
    c.run("docker ps -qa | xargs docker rm -f ")
    with c.cd("../regtest-workbench/"):
        c.run("./workbench.sh spawn ")
    c.run("docker cp alice.regtest.node:/data/certs/certificate.pem .")
    c.run("docker cp alice.regtest.node:/data/certs/access.macaroon .")
    c.run(
        "./main.py node.create-from-cert-files --network regtest --hostname localhost --mac-path access.macaroon --cert-path certificate.pem --node-type cln --protocol rest --rest-port 3001"
    )
