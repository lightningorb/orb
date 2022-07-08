# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-26 10:22:54
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-28 08:46:35

from fabric import Connection
from invoke import task
from pathlib import Path
import os


@task
def install(c, env=os.environ):
    c.run(f"pip3 install python-for-android", env=env)


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
    c.run("rm -f ~/orb/bin/*.apk")
    c.run("rm -f ~/orb/bin/*.aab")
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

    c.run(f"buildozer android debug", env=env)
    do_upload("*.apk")
    c.run(f"buildozer android release", env=env)
    do_upload("*.aab")


@task
def build_remote(c, env=os.environ):
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        with con.cd("orb"):
            con.run(
                f"./build.py android.build --AWS-ACCESS-KEY-ID {env['AWS_ACCESS_KEY_ID']} --AWS-SECRET-ACCESS-KEY  {env['AWS_SECRET_ACCESS_KEY']}"
            )


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
            con.run("git clean -f")
    c.run(
        "rsync -azv -e 'ssh -i lnorb_com.cer' . ubuntu@lnorb.com:/home/ubuntu/orb/ --exclude build --exclude dist --exclude .cache --exclude lnappstore/node_modules --exclude site/node_modules",
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
