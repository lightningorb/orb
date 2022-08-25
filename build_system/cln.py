# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-13 08:57:35
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-13 10:16:02

import os
from pathlib import Path

from invoke import task

releases = [
    "v0.11.2",
    "v0.11.1",
    "v0.11.0",
]


@task
def install_requirements(c, env=os.environ):
    c.run("pip3 install grpcio grpcio-tools googleapis-common-protos")


@task
def generate_grpc_libs(c, env=os.environ):
    c.run("mkdir -p tmp")
    protos = [
        "lightning/cln-grpc/proto/node.proto",
        "lightning/cln-grpc/proto/primitives.proto",
    ]

    with c.cd("tmp"):
        c.run(
            "git clone https://github.com/googleapis/googleapis.git", env=env, warn=True
        )
        c.run(
            "git clone https://github.com/ElementsProject/lightning.git",
            env=env,
            warn=True,
        )
        for release in releases:
            release_dir = release.replace(".", "_").replace("-", "_")
            c.run(f"rm -rf {release_dir}")
            c.run(f"mkdir -p {release_dir}")
            with c.cd("lightning"):
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


# @task
# def copy(c, env=os.environ):
#     c.run("")
