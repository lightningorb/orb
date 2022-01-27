# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:40:47
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-27 18:29:55

# build:
#     pyinstaller -y --clean --windowed orb.spec
#     cd dist && hdiutil create ./orb.dmg -srcfolder orb.app -ov
#     cp orb.ini dist/orb/

# spec:
#     pyinstaller -y --clean --windowed --name orb --exclude-module _tkinter --exclude-module Tkinter --exclude-module enchant   --exclude-module twisted main.py

from invoke import task
from pathlib import Path
import os

name = "lnorb"


@task
def requirements(c, env=dict(PATH=os.environ["PATH"])):
    c.run("pip3 install Kivy==2.1.0.dev0", env=env)
    c.run("pip3 install google-api-python-client", env=env)
    c.run("pip3 install grpcio", env=env)
    c.run("pip3 install ffpyplayer==4.2.0", env=env)
    c.run("pip3 install kivymd==0.104.2", env=env)
    c.run("pip3 install peewee==3.14.8", env=env)
    c.run("pip3 install python-dateutil==2.8.2", env=env)
    c.run("pip3 install kivy_garden.graph==0.4.0", env=env)
    c.run("pip3 install PyYaml==6.0", env=env)
    c.run("pip3 install simplejson==3.17.6", env=env)


@task
def pyarmor(c, env=dict(PATH=os.environ["PATH"])):
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


@task
def run(c, env=dict(PATH=os.environ["PATH"])):
    with c.cd("dist/"):
        c.run(f"./{name}")


@task
def dmg(c, env=dict(PATH=os.environ["PATH"])):
    # c.run("hdiutil create orb-pre-release.dmg -srcfolder dist -ov")
    c.run("rm -f *.dmg ")
    c.run(
        f"""
        create-dmg \
          --volname "Orb" \
          --background "images/bg.jpeg" \
          --volicon "icons/icns.icns" \
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


@task
def gen_license(c):
    print("pyarmor licenses --expired 2023-01-01 r001")


@task
def upload(c):
    c.run(
        "rsync -e 'ssh -i orbdb.cer' -azv --progress --partial lnorb.dmg ubuntu@lnorb.com:/home/ubuntu/releases/orb-osx-0.8.0.dmg"
    )
