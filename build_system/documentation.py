# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:36:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-03 17:56:24

import os
import re
import zipfile
from pathlib import Path
from fabric import Connection
from textwrap import dedent
from invoke import task


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), path),
            )


@task
def clean(c):
    """
    Delete the built docs. Useful when renaming modules etc.
    """
    c.run("rm -rf docs/docsbuild")


@task
def build_cli_docs(c, env=os.environ):
    c.run("pip3 install typer-cli", env=env)
    out = c.run("PYTHONPATH=. typer main.py utils docs --name orb", env=env).stdout
    out = out.replace("# `orb`", "")
    print("TYPER DOCS:")
    print(out)
    with open("docs/source/cli.md", "w") as f:
        f.write(out)
    c.run(
        "pandoc docs/source/cli.md --from markdown --to rst -s -o docs/source/cli.rst.tmp",
        env=env,
    )
    with open("docs/source/cli.rst.tmp") as f:
        tmp = ""
        lines = f.read().split("\n")
        for line in lines:
            if re.match(r"=+", line):
                line = "-" * len(line)
            if re.match(r"~+", line):
                line = "^" * len(line)
            tmp += line + "\n"
    print("PANDOC OUTPUT")
    print(tmp)
    with open("docs/source/cli.rst.template") as f:
        template = f.read()
    with open("docs/source/cli.rst", "w") as f:
        f.write(template)
        f.write("\n")
        f.write(tmp)

    c.run("pip3 uninstall --yes typer-cli", env=env)
    c.run("pip3 uninstall --yes typer[all]", env=env)
    c.run("pip3 install typer[all]", env=env)


@task
def build(c, env=os.environ):
    """
    Build the docs. Requires sphinx.
    """
    for app in Path("apps/").glob("*"):
        py = next(app.glob("*.py"))
        kv = next(app.glob("*.kv"), None)
        app = app.parts[-1]
        with open(f"docs/source/apps/{app}.rst", "w") as f:
            f.write(
                dedent(
                    f"""\
                {app}
                {len(app)*'='}

                appinfo.yaml
                ------------

                .. literalinclude:: ../../../apps/{app}/appinfo.yaml
                   :language: python


                {py.parts[-1]}
                {'-'*len(py.parts[-1])}

                .. literalinclude:: ../../../{py}
                   :language: python

                """
                )
            )
            if kv:
                f.write(
                    dedent(
                        f"""\
                {kv.parts[-1]}
                {'-'*len(kv.parts[-1])}

                .. literalinclude:: ../../../{kv}
                   :language: kivy
                    """
                    )
                )
    env["PYTHONPATH"] = "."
    parent_dir = Path(__file__).parent
    for p in (parent_dir / Path("third_party")).glob("*"):
        env["PYTHONPATH"] += f":{p.as_posix()}"
    flags = (
        "--ext-autodoc --module-first --follow-links --ext-coverage --separate --force"
    )
    c.run(
        f"sphinx-apidoc {flags} -o docs/source/gen/ orb orb/logic/licensing.py orb/misc/device_id.py orb/misc/sec_rsa.py",
        env=env,
    )
    c.run("sphinx-build -b html docs/source docs/docsbuild", env=env)


@task
def upload(c):
    """
    Upload docs to site.
    """
    zipf = zipfile.ZipFile("docs.zip", "w", zipfile.ZIP_DEFLATED)
    zipdir("docs/docsbuild", zipf)
    zipf.close()
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as c:
        c.run("rm -rf /home/ubuntu/lnorb_com/docs")
        c.run("mkdir -p /home/ubuntu/lnorb_com/docs")
        c.put("docs.zip", "/home/ubuntu/lnorb_com/docs")
        with c.cd("/home/ubuntu/lnorb_com/docs"):
            c.run("unzip docs.zip")


@task
def view(c):
    """
    View docs in the browser.
    """
    with c.cd("docs/docsbuild"):
        c.run("python3 -m http.server")


d = """\
Dockerfile
==========

.. code::

    FROM ubuntu:20.04

    RUN apt-get update
    RUN apt-get install curl -y

    RUN curl https://lnorb.s3.us-east-2.amazonaws.com/customer_builds/orb-<VERSION>-ubuntu-20.04-x86_64.tar.gz > orb-<VERSION>-ubuntu-20.04-x86_64.tar.gz 

    RUN tar xvf orb-<VERSION>-ubuntu-20.04-x86_64.tar.gz

    WORKDIR orb

    RUN apt-get update;
    ENV ORB_NO_DEVICE_ID_WARNING=1
    ARG DEBIAN_FRONTEND=noninteractive
    RUN bash bootstrap_ubuntu_20_04.sh

Then some commands to get you started:

.. code::

    docker build -t orb .
    alias orb='docker run --rm -v `pwd`/orb_data:/root/.config -p 8080:8080 -it orb python3.9 main.py ${*}'
    orb --help
    orb test run-all-tests
    orb node create-orb-public cln rest
    orb node info
    orb node create-orb-public lnd rest
    orb web serve
"""


@task
def dockerfile(c):
    """
    Write the Dockerfile docs.
    """
    global d
    with open("VERSION") as f:
        version = f.read().strip()
        d = d.replace("<VERSION>", version)
        with open("docs/source/dockerfile.rst", "w") as w:
            w.write(d)
