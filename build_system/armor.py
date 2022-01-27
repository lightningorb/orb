# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:46:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-28 07:19:42

from invoke import task
from pathlib import Path

name = "lnorb"


@task
def register(c, env=dict(PATH=os.environ["PATH"])):
    c.run("pyarmor register pyarmor-regcode-2364.txt", env=env)


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
