# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:36:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-24 10:52:27

import os
import re
from pathlib import Path
from fabric import Connection
from textwrap import dedent
from invoke import task


@task
def clean(c):
    """
    Delete the built docs. Useful when renaming modules etc.
    """
    c.run("rm -rf docs/docsbuild")


@task
def build_cli_docs(c, env=os.environ):
    c.run("pip3 install typer[all]", env=env)
    c.run("pip3 install typer-cli")
    c.run("PYTHONPATH=. ./build_system/typer main.py utils docs --name orb", env=env)
    with open("docs/source/cli.rst.template") as f:
        template = f.read()
    with open("docs/source/cli/cli_toc.rst") as f:
        ref = f.read()
    with open("docs/source/cli.rst", "w") as f:
        f.write(template)
        f.write("\n")
        f.write(ref)
    c.run("pip3 uninstall --yes typer-cli", env=env)
    c.run("pip3 uninstall --yes typer[all]", env=env)
    c.run("pip3 install typer[all]", env=env)


@task
def build(c, api_doc: bool = True, env=os.environ):
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
    if api_doc:
        flags = "--ext-autodoc --module-first --follow-links --ext-coverage --separate --force"
        c.run(
            f"sphinx-apidoc {flags} -o docs/source/gen/ orb orb/logic/licensing.py orb/misc/device_id.py orb/misc/sec_rsa.py",
            env=env,
        )
    c.run("sphinx-build -b html docs/source docs/docsbuild", env=env)


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
def asciinema(c, script: str = None):
    casts = [Path(script)] if script else Path("build_system/casts").glob("*.sh")
    for cast in casts:
        print(cast)
        out = Path("docs/source/_static/") / cast.with_suffix(".cast").name
        c.run(
            f"orb node create-orb-public lnd rest",
            env=os.environ,
        )
        cast = cast.resolve()
        out = out.resolve()
        home = os.path.expanduser("~")
        os.chdir(home)

        addr = "tb1q8xf4zl65qtvlqrk6d8p4f46al3yzyqj7ypg5n7"
        pubkey = "031ce6d59ad4fe4158949dcd87ea49158dc6923f4457ec69bae9b0b04c13973213"
        os.environ["addr"] = addr
        os.environ["pubkey"] = pubkey
        os.environ[
            "MAC_HEX"
        ] = "0201036c6e6402f801030a106fb784f1598e0ce2f89c050b98139c8e1201301a160a0761646472657373120472656164120577726974651a130a04696e666f120472656164120577726974651a170a08696e766f69636573120472656164120577726974651a210a086d616361726f6f6e120867656e6572617465120472656164120577726974651a160a076d657373616765120472656164120577726974651a170a086f6666636861696e120472656164120577726974651a160a076f6e636861696e120472656164120577726974651a140a057065657273120472656164120577726974651a180a067369676e6572120867656e6572617465120472656164000006205d186c6864b437cd5d723eef6d064eae85467e7913f876a8b49bfe962028a2e8"
        os.environ[
            "CERT_HEX"
        ] = "2d2d2d2d2d424547494e2043455254494649434154452d2d2d2d2d0a4d4949434f6a434341654367417749424167495145334d79326731673579527344333576322f34716644414b42676771686b6a4f50515144416a41344d5238770a485159445651514b45785a73626d5167595856306232646c626d56795958526c5a43426a5a584a304d5255774577594456515144457777344e6a42695954566a0a4e5451334e7a41774868634e4d6a49774f4449774d6a45314d4451315768634e4d6a4d784d4445314d6a45314d445131576a41344d523877485159445651514b0a45785a73626d5167595856306232646c626d56795958526c5a43426a5a584a304d5255774577594456515144457777344e6a42695954566a4e5451334e7a41770a5754415442676371686b6a4f5051494242676771686b6a4f50514d4242774e43414152526e534b7933754e565672515857687845486f54587a777143753459430a6453524456715179724a77523331334f70305343685a5a616e5a7869676a46424b6c61706d51764e52793149684e5578646b4e32655451346f34484c4d4948490a4d41344741315564447745422f775145417749437044415442674e56485355454444414b4267677242674546425163444154415042674e5648524d42416638450a425441444151482f4d42304741315564446751574242547534795467394a30316c33726f6a457a5369445364335246777a7a427842674e5648524545616a426f0a676777344e6a42695954566a4e5451334e7a434343577876593246736147397a6449495563326c6e626d56304c6d78755a433573626d39795969356a623232430a4248567561586943436e56756158687759574e725a58534342324a315a6d4e76626d3648424838414141474845414141414141414141414141414141414141410a41414748424b775741415177436759494b6f5a497a6a30454177494453414177525149676377525376544e714a5072563678642b53464b5a566738416a4951770a6a59635136644e51305039775479454349514434566a3361632b622b33357456656459525835734f4a374b5741456448656d77766c354f515334456733773d3d0a2d2d2d2d2d454e442043455254494649434154452d2d2d2d2d"

        with c.cd(home):
            c.run(
                f"asciinema-automation -aa '-i 0.5 --overwrite' -dt 1 {cast} {out}",
                env=os.environ,
            )
            print(out)
