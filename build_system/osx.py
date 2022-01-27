# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:40:47
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-28 05:46:51

from invoke import task
import os

name = "lnorb"


@task
def requirements(c, env=dict(PATH=os.environ["PATH"])):
    c.run("pip3 install requirements.txt --user")


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
