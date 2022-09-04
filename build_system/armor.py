# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:46:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-03 19:29:32

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


def upload_to_s3(env, file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"],
    )
    try:
        response = s3_client.upload_file(
            file_name, bucket, object_name, ExtraArgs={"ACL": "public-read"}
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), path),
            )


@task
def register(c, env=os.environ):
    c.run("pyarmor register pyarmor-regcode-2364.txt", env=env)


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
    register(c)
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

    data = " ".join(f"--add-data '{s}{sep}{d}'" for s, d in data)
    print("=" * 50)
    print("DATA PATHS")
    print(data)
    print("=" * 50)
    hidden_imports = "--hidden-import orb.orb_main --hidden-import orb.core --hidden-import orb.core_ui.hidden_imports --hidden-import kivy --hidden-import plyer.platforms.macosx.uniqueid --hidden-import orb.core_ui.kvs --hidden-import orb.misc --hidden-import jaraco.text --hidden-import kivymd.effects.stiffscroll.StiffScrollEffect  --hidden-import fabric --hidden-import=pkg_resources"  # --hidden-import pandas.plotting._matplotlib
    pyinstall_flags = f" {paths} {data} {hidden_imports} --onedir --{'windowed' if sep == ':' else 'console'} "
    expiry = arrow.utcnow().shift(years=1)
    c.run(
        f"pyarmor licenses --expired {expiry.format('YYYY-MM-DD')} satoshi_0_paid",
        env=os.environ,
    )
    c.run(
        f"""pyarmor pack {spec} --with-license licenses/satoshi_0_paid/license.lic --name {name} \
             -e " {pyinstall_flags}" \
             -x " --no-cross-protection --exclude build --exclude orb/lnd/grpc_generated" main.py""",
        env=env,
    )


@task
def build_linux(c, do_upload=True, env=os.environ):
    register(c)
    c.run("rm -rf dist tmp;")
    c.run("mkdir -p tmp;")
    c.run("cp -r main.py tmp/;")
    c.run("cp -r third_party tmp/;")
    c.run("cp -r orb tmp/;")
    with c.cd("tmp"):
        expiry = arrow.utcnow().shift(years=1)
        c.run(
            f"pyarmor licenses --expired {expiry.format('YYYY-MM-DD')} satoshi_0_paid",
            env=os.environ,
        )
        c.run(
            "pyarmor obfuscate --with-license licenses/satoshi_0_paid/license.lic --recursive main.py;",
            env=env,
        )
        c.run("rm -rf orb main.py third_party")
        c.run("mv dist orb")
        for source, target in data:
            c.run(f"mkdir -p orb/{target}")
            c.run(f"cp -r ../{source} orb/{target}")
        with c.cd("orb"):
            c.run("python main.py test run-all-tests")

        with open("tmp/orb/bootstrap_ubuntu_20_04.sh", "w") as f:
            f.write(ubuntu_boostrap_3_8())
        build_name = (
            f"orb-{VERSION}-{os.environ.get('os-name', 'undefined')}-x86_64.tar.gz"
        )
        c.run(f"tar czvf {build_name} orb;")
        if do_upload:
            upload_to_s3(
                env,
                f"tmp/{build_name}",
                "lnorb",
                object_name=f"customer_builds/{build_name}",
            )


@task
def build_osx(c, do_upload=True, env=os.environ):
    build_common(c=c, env=env, sep=":")
    file_name = dmg(c=c, env=env)
    with c.cd("dist/lnorb"):
        c.run("./lnorb test run-all-tests")
    if do_upload:
        print(f"Uploading {file_name} to S3: customer_builds/{file_name}")
        upload_to_s3(
            env, file_name, "lnorb", object_name=f"customer_builds/{file_name}"
        )


@task
def build_windows(c, env=os.environ):
    build_common(c, env, ";")
    build_name = f"orb-{VERSION}-{os.environ['os-name']}-x86_64.zip"
    zipf = zipfile.ZipFile(build_name, "w", zipfile.ZIP_DEFLATED)
    # for p in Path(".").glob("*.spec"):
    #     print(p)
    #     print(p.open().read())
    # shutil.copyfile(p.as_posix(), "dist")
    with c.cd("dist/lnorb"):
        c.run("lnorb.exe test run-all-tests")
    zipdir("dist", zipf)
    zipf.close()
    upload_to_s3(env, build_name, "lnorb", object_name=f"customer_builds/{build_name}")


def dmg(c, env=os.environ):
    c.run("rm -f *.dmg ")
    c.run(
        f"""
        create-dmg \
          --volname "Orb" \
          --background "images/bg.jpeg" \
          --window-pos 200 120 \
          --window-size 800 400 \
          --icon-size 100 \
          --icon "lnorb.app" 200 190 \
          --app-drop-link 600 185 \
          "{name}.dmg" \
          "dist/{name}.app"
        """,
        env=env,
    )
    build_name = f"orb-{VERSION}-{os.environ.get('os-name', 'macos-11')}-x86_64.dmg"
    os.rename(f"{name}.dmg", build_name)
    return build_name
