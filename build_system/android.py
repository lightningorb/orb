# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-26 10:22:54
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-13 12:14:21

from fabric import Connection
from invoke import task, Responder
from pathlib import Path
from textwrap import dedent
import os

to_compile = set(
    [
        "orb/lnd/lnd.py",
        "orb/lnd/lnd_base.py",
        "orb/lnd/lnd_grpc.py",
        "orb/lnd/lnd_rest.py",
        "orb/misc/sec_rsa.py",
        "orb/misc/certificate.py",
        "orb/misc/certificate_secure.py",
        "orb/misc/macaroon.py",
        "orb/misc/macaroon_secure.py",
        "orb/misc/device_id.py",
        # "orb/misc/channels.py",
        "orb/misc/decrypt.py",
        "orb/logic/balanced_ratio.py",
        "orb/math/lerp.py",
        "orb/math/normal_distribution.py",
        "orb/math/Vector.py",
    ]
)


@task
def install(c, env=os.environ):
    c.run(f"pip3 install python-for-android", env=env)


@task
def minify(c, env=os.environ):
    for p in Path("orb/").rglob("*.py"):
        c.run(f"/home/ubuntu/.local/bin/pyminify {p} --in-place")


def get_obf_py_files():
    ignore = "grpc_generated"
    dirs = [
        "orb/store",
        "orb/math",
        "orb/widgets",
        "orb/status_line",
        "orb/screens",
        "orb/logic",
        "orb/dialogs",
        "orb/attribute_editor",
        "orb/audio",
        "orb/channels",
        "orb/components",
        "orb/core",
        "orb/core_ui",
        "orb/lnd",
    ]
    ret = []
    for _dir in dirs:
        for p in Path(_dir).rglob("*.py"):
            if ignore in str(p):
                continue
            if "__init__.py" in str(p):
                continue
            if str(p) not in to_compile:
                ret.append(p)
    return ret


@task
def obfuscate(c, env=os.environ):
    import base64
    from orb.misc.decrypt import encrypt

    for p in get_obf_py_files():
        if str(p) not in to_compile:
            print(f"Obfuscate: {p}")
            with p.open() as f:
                code = f.read()
                b64code = encrypt(code)
            with p.open("w") as f:
                f.write(
                    dedent(
                        f"""\
                        from orb.misc.decrypt import decrypt
                        eval(decrypt({b64code}))
                        """
                    )
                )
        else:
            print(f"Compile: {p}")


@task
def build(
    c,
    env=os.environ,
    AWS_ACCESS_KEY_ID=None,
    AWS_SECRET_ACCESS_KEY=None,
):
    """
    need to set sqlite version to 3.38.0 or SQLITE_ENABLE_JSON1=1
    ~/orb/.buildozer/android/platform/python-for-android/pythonforandroid/recipes/sqlite3/__init__.py
    """
    # c.run("mkdir -p ~/orb/.buildozer/android/platform")
    # c.run(
    #     "cp -r ~/pythonforandroid ~/orb/.buildozer/android/platform/python-for-android/"
    # )
    # minify(c, env=env)
    c.run("rm -rf ~/orb/bin/*")
    c.run("rm -rf ~/orb/tmp*")
    env[
        "PATH"
    ] = "/home/ubuntu/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

    def do_upload(ext):
        build_name = next(iter(Path("bin/").glob(ext)), None)
        if build_name:
            upload_to_s3(
                env,
                build_name.as_posix(),
                "lnorb",
                AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID,
                AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY,
                object_name=f"customer_builds/{build_name.name}",
            )

    # stdout = c.run(f"buildozer android debug", env=env).stdout
    # stdout = c.run(f"buildozer android release", env=env).stdout
    # do_upload("*.apk")
    c.run(f"buildozer android release", env=env)
    c.run("cp -f ~/orb/bin/* ~/lnorb_com/")
    # do_upload("*.aab")


@task
def sign(
    c,
    release_path="/home/ubuntu/orb/bin/orb-0.16.0.0-arm64-v8a_armeabi-v7a-release.aab",
    password="",
):
    keystore_path = "/home/ubuntu/keystores/com.orb.orb.keystore"
    aligned_path = Path(release_path).with_suffix(
        f".aligned{Path(release_path).suffix}"
    )
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        responder = Responder(
            pattern=r"Enter Passphrase for keystore:.*",
            response=password,
        )
        con.run(
            f"jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore {keystore_path} {release_path} cb-play",
            watchers=[responder],
        )
        if con.run(f"test -f {aligned_path}", warn=True).ok:
            con.run(f"rm {aligned_path}")
        con.run(
            f"/home/ubuntu/.buildozer/android/platform/android-sdk/build-tools/33.0.0/zipalign -v 4 {release_path} {aligned_path}"
        )
        con.get(aligned_path, os.path.expanduser("~/Downloads/"))


@task
def create_keystore(c):
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        if c.run("test -d ~/keystores/com.orb.orb.keystore", warn=True).failed:
            raise Exception("Key not yet created - please create it")
            c.run(
                "keytool -genkey -v -keystore ./keystores/com.orb.orb.keystore -alias cb-play -keyalg RSA -keysize 2048 -validity 10000"
            )


@task
def build_remote(c, env=os.environ):
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        with con.cd("orb"):
            con.run(
                f"./build.py android.obfuscate android.cython android.cython-obfuscated android.build --AWS-ACCESS-KEY-ID {env['AWS_ACCESS_KEY_ID']} --AWS-SECRET-ACCESS-KEY  {env['AWS_SECRET_ACCESS_KEY']}"
            )


@task
def cython(c, env=os.environ):
    """
    In this task, we loop through non-obfuscated py files that are cythonable,
    and generate their pyx equivalent. It's important to seed UUID else
    we'll keep on generating new pyx files each time, that'll need to be
    rebuilt each time.
    """
    import uuid
    import random as rd

    rd.seed(0)

    for p in to_compile:
        p = Path(p)
        uid = "m" + str(uuid.UUID(int=rd.getrandbits(128))).replace("-", "_")
        pyx = f"/home/ubuntu/orb/lib/custom_lib/{uid}.pyx"
        c.run(f"cp /home/ubuntu/orb/{str(p)} {pyx}")
        cmd = f"sed -i '1s/^/# cython: language_level=3\\n/' {pyx}"
        c.run(cmd)
        c.run(f"echo 'from {uid} import *' > /home/ubuntu/orb/{str(p)}")


@task
def cython_obfuscated(c, env=os.environ):
    """
    In this task, we loop through obfuscated py files,
    and generate their pyx equivalent. It's important to seed UUID else
    we'll keep on generating new pyx files each time, that'll need to be
    rebuilt each time.
    """
    import uuid
    import random as rd

    rd.seed(1)

    for p in get_obf_py_files():
        uid = "m" + str(uuid.UUID(int=rd.getrandbits(128))).replace("-", "_")
        pyx = f"/home/ubuntu/orb/lib/custom_lib/{uid}.pyx"
        c.run(f"cp /home/ubuntu/orb/{str(p)} {pyx}")
        cmd = f"sed -i '1s/^/# cython: language_level=3\\n/' {pyx}"
        c.run(cmd)
        c.run(f"echo 'from {uid} import *' > /home/ubuntu/orb/{str(p)}")


@task
def clean(c, env=os.environ):
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        with con.cd("orb"):
            con.run("rm -rf .buildozer")


@task
def sync(c, env=os.environ):
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        with con.cd("orb"):
            con.run("git reset --hard")
            con.run("git clean -fd")
    c.run(
        "rsync -azv -e 'ssh -i lnorb_com.cer' . ubuntu@lnorb.com:/home/ubuntu/orb/ --exclude build --exclude dist --exclude .cache --exclude lnappstore/node_modules --exclude site/node_modules --exclude *.dmg",
        env=env,
    )


def upload_to_s3(
    env,
    file_name,
    bucket,
    object_name=None,
    AWS_ACCESS_KEY_ID=None,
    AWS_SECRET_ACCESS_KEY=None,
):
    import boto3
    from botocore.exceptions import ClientError

    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    try:
        response = s3_client.upload_file(
            file_name, bucket, object_name, ExtraArgs={"ACL": "public-read"}
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True
