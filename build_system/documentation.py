# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:36:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-01 12:30:58

import os
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
    with open("docs/source/cli.md", "w") as f:
        f.write(out)
    c.run(
        "which pandoc",
        env=env,
    )
    c.run("pandoc --help", env=env)
    c.run(
        "pandoc docs/source/cli.md --from markdown --to rst -s -o docs/source/cli.rst.tmp",
        env=env,
    )
    with open("docs/source/cli.rst.tmp") as f:
        tmp = f.read()
    with open("docs/source/cli.rst.template") as f:
        template = f.read()
    with open("docs/source/cli.rst", "w") as f:
        f.write(template)
        f.write("\n")
        f.write(tmp)

    os.unlink("docs/source/cli.rst.tmp")

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
