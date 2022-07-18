# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-18 06:41:44
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-18 08:35:53

import os
from pathlib import Path

from invoke import task


@task
def install_requirements(c, env=os.environ):
    c.run("pip3 install grpcio grpcio-tools googleapis-common-protos")


@task
def generate_grpc_libs(c, env=os.environ):
    c.run("mkdir -p tmp")
    protos = [
        "lnd/lnrpc/lightning.proto",
        "lnd/lnrpc/invoicesrpc/invoices.proto",
        "lnd/lnrpc/routerrpc/router.proto",
    ]
    releases = [
        "v0.14.0-beta",
        "v0.14.1-beta",
        "v0.14.2-beta",
        "v0.14.3-beta",
        "v0.15.0-beta",
    ]
    with c.cd("tmp"):
        c.run(
            "git clone https://github.com/googleapis/googleapis.git", env=env, warn=True
        )
        c.run(
            "git clone https://github.com/lightningnetwork/lnd.git", env=env, warn=True
        )
        for release in releases:
            release_dir = release.replace(".", "_").replace("-", "_")
            c.run(f"rm -rf {release_dir}")
            c.run(f"mkdir -p {release_dir}")
            with c.cd("lnd"):
                c.run(f"git checkout {release}")
            c.run("rm -f *.py *.proto")
            for proto in protos:
                c.run(f"cp {proto} .")
            for proto in protos:
                c.run(
                    f"python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. {Path(proto).name}",
                    env=env,
                )
                c.run(f"mv *.py {release_dir}")
