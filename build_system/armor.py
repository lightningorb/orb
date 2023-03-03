# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:46:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2023-02-08 13:25:02

try:
    # not all actions install all requirements
    import os
    from invoke import task
    from pathlib import Path
    import requests
    import zipfile
    from fabric import Connection
    import git
    import yaml
    import logging
    import boto3
    from botocore.exceptions import ClientError
    import rsa
    import arrow
except Exception as e:
    print(e)
    pass

name = "lnorb"
VERSION = open("VERSION").read().strip()

data = [
    ("orb/lnd/grpc_generated", "orb/lnd/grpc_generated"),
    ("orb/audio/link_fail_event.wav", "orb/audio/"),
    ("orb/audio/forward_settle.wav", "orb/audio/"),
    ("orb/audio/send_settle.wav", "orb/audio/"),
    ("orb/images/shadow_inverted.png", "orb/images/"),
    ("orb/misc/settings.json", "orb/misc/"),
    (
        "orb/web/orb_frontend/public/build/bundle.css",
        "orb/web/orb_frontend/public/build/",
    ),
    (
        "orb/web/orb_frontend/public/build/bundle.js",
        "orb/web/orb_frontend/public/build/",
    ),
    (
        "orb/web/orb_frontend/public/build/bundle.js.map",
        "orb/web/orb_frontend/public/build/",
    ),
    (
        "orb/web/orb_frontend/public/favicon.png",
        "orb/web/orb_frontend/public/",
    ),
    (
        "orb/web/orb_frontend/public/global.css",
        "orb/web/orb_frontend/public/",
    ),
    (
        "orb/web/orb_frontend/public/index.html",
        "orb/web/orb_frontend/public/",
    ),
    ("orb/apps/auto_fees/autofees.py", "orb/apps/auto_fees/"),
    ("orb/apps/auto_fees/autofees.kv", "orb/apps/auto_fees/"),
    ("orb/apps/auto_fees/autofees.png", "orb/apps/auto_fees/"),
    ("orb/apps/auto_fees/appinfo.yaml", "orb/apps/auto_fees/"),
    ("orb/apps/auto_rebalance/autobalance.py", "orb/apps/auto_rebalance/"),
    ("orb/apps/auto_rebalance/autobalance.kv", "orb/apps/auto_rebalance/"),
    ("orb/apps/auto_rebalance/autobalance.png", "orb/apps/auto_rebalance/"),
    ("orb/apps/auto_rebalance/appinfo.yaml", "orb/apps/auto_rebalance/"),
    ("orb/apps/auto_max_htlcs/update_max_htlc.py", "orb/apps/auto_max_htlcs/"),
    ("orb/apps/auto_max_htlcs/update_max_htlcs.png", "orb/apps/auto_max_htlcs/"),
    ("orb/apps/auto_max_htlcs/appinfo.yaml", "orb/apps/auto_max_htlcs/"),
    ("tests", "tests"),
    ("VERSION", "."),
    ("images/ln.png", "images/"),
]


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), path),
            )


def ubuntu_boostrap_3_8():
    return """\
#!/bin/bash

sudo apt-get update;
sudo apt-get -y install python3-pip xsel libffi-dev software-properties-common;
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
pip install kivymd==0.104.2;
pip install peewee==3.14.8;
pip install python-dateutil==2.8.2;
pip install kivy_garden.graph==0.4.0;
pip install PyYaml==6.0;
pip install simplejson==3.17.6;
pip install Kivy==2.1.0;
pip install google-api-python-client;
pip install grpcio
pip install python-dateutil==2.8.2;
pip install pyinstaller==4.9;
pip install pyarmor==6.6.2;
pip install fabric;
pip install plyer;
pip install fastapi;
pip install uvicorn;
pip install rich;
pip install typer;
pip install uvicorn;
pip install simple_chalk;
pip install bech32;
pip install semver;
pip install memoization;
pip install pytest;
pip install --force-reinstall --no-binary :all: cffi
pip install --upgrade --force-reinstall pillow
    """


def build_common(c, env, sep=":"):
    global data
    spec = ""
    if sep == ";":
        # windows detected
        spec = "-s lnorb-win-patched.spec"
    paths = " ".join(
        [
            f"--paths={x.as_posix()}"
            for x in Path("third_party/").glob("*")
            if x.is_dir()
        ]
    )
    data = " ".join(f"--add-data {s}{sep}{d}" for s, d in data)
    hidden_imports = "--hidden-import orb.orb_main --hidden-import orb.core --hidden-import orb.core_ui.hidden_imports --hidden-import kivy --hidden-import plyer.platforms.macosx.uniqueid --hidden-import orb.core_ui.kvs --hidden-import orb.misc --hidden-import jaraco.text --hidden-import kivymd.effects.stiffscroll.StiffScrollEffect  --hidden-import fabric --hidden-import=pkg_resources"  # --hidden-import pandas.plotting._matplotlib
    pyinstall_flags = f" -y {paths} {data} {hidden_imports} --onedir --{'windowed' if sep == ':' else 'console'} --name lnorb"

    print("=" * 50)
    print(pyinstall_flags)
    print("=" * 50)

    c.run(f"pyinstaller {pyinstall_flags} main.py")


@task
def build_linux(c, do_upload=True, env=os.environ):
    c.run("rm -rf dist tmp;")
    c.run("mkdir -p tmp/orb/;")
    c.run("cp -r main.py tmp/orb/;")
    c.run("cp -r third_party tmp/orb/;")
    c.run("cp -r orb tmp/orb/;")
    with c.cd("tmp"):
        for source, target in data:
            c.run(f"mkdir -p {target}")
            c.run(f"cp -r ../{source} orb/{target}")
        # with c.cd("orb"):
        # c.run("python main.py test run-all-tests")
        with open("tmp/orb/bootstrap_ubuntu_20_04.sh", "w") as f:
            f.write(ubuntu_boostrap_3_8())
        build_name = (
            f"orb-{VERSION}-{os.environ.get('os-name', 'undefined')}-x86_64.tar.gz"
        )
        print(f"BUILD NAME: {build_name}")
        c.run(f"tar czvf ../{build_name} .;")


@task
def build_osx(c, do_upload=True, env=os.environ):
    build_common(c=c, env=env, sep=":")
    dmg(c, env=env)


@task
def build_windows(c, env=os.environ):
    build_common(c, env, ";")
    build_name = f"orb-{VERSION}-{os.environ['os-name']}-x86_64.zip"
    zipf = zipfile.ZipFile(build_name, "w", zipfile.ZIP_DEFLATED)
    with c.cd("dist/lnorb"):
        c.run("lnorb.exe test run-all-tests")
    zipdir("dist", zipf)
    zipf.close()


@task
def dmg(c, env=os.environ):
    c.run("ls -l . ")
    c.run("ls -l dist/ ")
    c.run("rm -f *.dmg ")
    c.run(
        f"""
        create-dmg \
          --volname "Orb" \
          --background "images/bg.jpeg" \
          --window-pos 200 120 \
          --window-size 800 400 \
          --icon-size 100 \
          --icon "lnorb" 200 190 \
          --app-drop-link 600 185 \
          "{name}.dmg" \
          "dist/lnorb.app"
        """,
        env=env,
    )
    build_name = f"orb-{VERSION}-{os.environ.get('os-name', 'macos-11')}-x86_64.dmg"
    os.rename(f"{name}.dmg", build_name)
    return build_name


@task
def build_docker(c, env=os.environ):
    OS_NAME = env["os-name"]
    assert OS_NAME
    ORB_VERSION = open("VERSION").read().strip()
    DOCKERHUB_USERNAME = env["DOCKERHUB_USERNAME"]
    DOCKERHUB_PASSWORD = env["DOCKERHUB_PASSWORD"]
    r = c.run
    docker = lambda cmd: r(f"docker {cmd}", env=env)

    # log in
    docker(f"login -u {DOCKERHUB_USERNAME} -p {DOCKERHUB_PASSWORD}")

    # build: lnorb/orb:0.21.12
    cmd = f"build --build-arg ORB_VERSION={ORB_VERSION} --build-arg OS_NAME={OS_NAME} -t lnorb/orb:{ORB_VERSION} ."
    print("CMD:")
    print(cmd)
    docker(cmd)
    docker(f"push lnorb/orb:{ORB_VERSION}")

    variants = ["latest", f"{OS_NAME}_latest", f"{OS_NAME}_{ORB_VERSION}"]

    for v in variants:
        docker(f"tag lnorb/orb:{ORB_VERSION} lnorb/orb:{v}")
        docker(f"push lnorb/orb:{v}")
