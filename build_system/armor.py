# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:46:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-29 04:35:06

from invoke import task
from pathlib import Path

import os

name = "lnorb"


@task
def register(c, env=os.environ):
    c.run("pyarmor register pyarmor-regcode-2364.txt", env=env)


def ubuntu_instructions_3_9():
    return """\
    sudo apt-get update
    sudo apt-get -y install python3-pip
    sudo apt update -y
    sudo apt install software-properties-common  -y
    sudo add-apt-repository ppa:deadsnakes/ppa  -y
    sudo apt install python3.9  -y
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python3.9 get-pip.py
    pip3.9 install kivymd==0.104.2 --user;
    pip3.9 install peewee==3.14.8 --user;
    pip3.9 install python-dateutil==2.8.2 --user;
    pip3.9 install kivy_garden.graph==0.4.0 --user;
    pip3.9 install PyYaml==6.0 --user;
    pip3.9 install simplejson==3.17.6 --user;
    pip3.9 install Kivy==2.0.0 --user;
    pip3.9 install google-api-python-client --user;
    pip3.9 install grpcio --user;
    pip3.9 install ffpyplayer==4.2.0 --user;
    pip3.9 install python-dateutil==2.8.2 --user;
    pip3.9 install pyinstaller --user;
    pip3.9 install pyarmor==6.6.2 --user;
    pip3.9 install fabric --user;
    pip3.9 install plyer --user;
    pip3.9 install semver --user;
    """


def ubuntu_instructions_3():
    return """\
    sudo apt-get update -y
    sudo apt-get -y install python3-pip
    pip3 install kivymd==0.104.2 --user;
    pip3 install peewee==3.14.8 --user;
    pip3 install python-dateutil==2.8.2 --user;
    pip3 install kivy_garden.graph==0.4.0 --user;
    pip3 install PyYaml==6.0 --user;
    pip3 install simplejson==3.17.6 --user;
    pip3 install Kivy==2.0.0 --user;
    pip3 install google-api-python-client --user;
    pip3 install grpcio --user;
    pip3 install ffpyplayer==4.2.0 --user;
    pip3 install python-dateutil==2.8.2 --user;
    pip3 install pyinstaller --user;
    pip3 install pyarmor==6.6.2 --user;
    pip3 install fabric --user;
    pip3 install plyer --user;
    pip3 install semver --user;
    """


@task
def obf(c, env=os.environ):
    c.run("rm -rf dist tmp;")
    c.run("mkdir -p tmp;")
    c.run("cp -r main.py tmp/;")
    c.run("cp -r third_party tmp/;")
    c.run("cp -r orb tmp/;")
    with c.cd("tmp"):
        c.run(
            "pyarmor obfuscate --with-license ../licenses/r003/license.lic --recursive main.py;",
            env=env,
        )
        with open("tmp/dist/instructions.txt", "w") as f:
            f.write(ubuntu_instructions_3())
        c.run("mv dist orb")
        c.run("tar czvf orb-0.8.0-ubuntu.tar.gz orb;")
    c.run("rm -rf src")


@task
def build(c, env=dict(PATH=os.environ["PATH"])):
    c.run("rm -rf dist")
    paths = " ".join(
        [
            f"--paths={x.as_posix()}"
            for x in Path("third_party/").glob("*")
            if x.is_dir()
        ]
    )

    data = [
        ("orb/lnd/grpc_generated", "orb/lnd/grpc_generated"),
        ("orb/images/shadow_inverted.png", "orb/images/"),
        ("orb/misc/settings.json", "orb/misc/"),
        ("video_library.yaml", "."),
        ("images/ln.png", "."),
    ]
    data = " ".join(f"--add-data '{s}:{d}'" for s, d in data)
    hidden_imports = "--hidden-import orb.misc --hidden-import kivymd.effects.stiffscroll.StiffScrollEffect --hidden-import pandas.plotting._matplotlib --hidden-import=pkg_resources"
    pyinstall_flags = f" {paths} {data} {hidden_imports} --onedir --windowed "  #  --osx-bundle-identifier lnorb.com --codesign-identity C5B3E44CB245D5BF2A0EF5DD4948FF9C4BB42627
    print(
        f"""pyarmor pack --with-license licenses/r003/license.lic --name {name} \
             -e " {pyinstall_flags}" \
             -x " --no-cross-protection --exclude build --exclude orb/lnd/grpc_generated" main.py"""
    )
