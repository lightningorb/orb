# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-26 10:22:54
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-03 15:17:26

import os
from hashlib import sha256
from pathlib import Path
from textwrap import dedent

from fabric import Connection
from invoke import task, Responder

to_compile = set(
    [
        "orb/orb_main.py",
        "orb/lnd/lnd.py",
        "orb/lnd/lnd_base.py",
        "orb/lnd/lnd_grpc.py",
        "orb/lnd/lnd_rest.py",
        "orb/dialogs/forwarding_history.py",
        "orb/math/lerp.py",
        "orb/math/normal_distribution.py",
        "orb/math/Vector.py",
    ]
)

for p in [
    "attribute_editor",
    "audio",
    "channels",
    "components",
    "core",
    "core_ui",
    "dialogs",
    "lnd",
    "screens",
    "logic",
    "math",
    "misc",
    "screens",
    "status_line",
    "store",
    "widgets",
    "connector",
]:
    to_compile |= set(
        [
            x.as_posix()
            for x in Path(f"orb/{p}").rglob("*.py")
            if "grpc_generated" not in x.as_posix() and "__init__" not in x.as_posix()
        ]
    )


@task
def install(c, env=os.environ):
    c.run(f"pip3 install python-for-android", env=env)


def upload_to_site(path):
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as c:
        name = Path(path).name
        c.run(f"rm -f /home/ubuntu/lnorb_com/{name}", warn=True)
        print(f"Uploading: {path}")
        c.put(path, "/home/ubuntu/lnorb_com/")


@task
def deploy(
    c,
):
    import os
    import json
    from urllib import request, parse
    import googleapiclient.discovery
    from google.oauth2 import service_account

    path = sign(c)

    SCOPES = ["https://www.googleapis.com/auth/androidpublisher"]

    with open("pc-api-6008359505353802256-381-7c4cef527151.json", "w") as f:
        f.write(os.environ["PCAPI"])

    SERVICE_ACCOUNT_FILE = "pc-api-6008359505353802256-381-7c4cef527151.json"
    APP_BUNDLE = path

    package_name = "com.lnorb.orb"

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = googleapiclient.discovery.build(
        "androidpublisher", "v3", credentials=credentials, cache_discovery=False
    )
    edit_request = service.edits().insert(body={}, packageName=package_name)
    result = edit_request.execute()
    edit_id = result["id"]

    print(edit_id)

    try:
        bundle_response = (
            service.edits()
            .bundles()
            .upload(
                editId=edit_id,
                packageName=package_name,
                media_body=APP_BUNDLE,
                media_mime_type="application/octet-stream",
            )
            .execute()
        )
    except Exception as err:
        message = f"There was an error while uploading a new version of {package_name}"
        raise err

    print(f"Version code {bundle_response['versionCode']} has been uploaded")

    track_response = (
        service.edits()
        .tracks()
        .update(
            editId=edit_id,
            track="beta",
            packageName=package_name,
            body={
                "releases": [
                    {
                        "versionCodes": [str(bundle_response["versionCode"])],
                        "status": "completed",
                    }
                ]
            },
        )
        .execute()
    )

    print("The bundle has been committed to the beta track")

    #   Create a commit request to commit the edit to BETA track
    commit_request = (
        service.edits().commit(editId=edit_id, packageName=package_name).execute()
    )

    print(f"Edit {commit_request['id']} has been committed")

    message = f"Version code {bundle_response['versionCode']} has been uploaded from the bucket {bucket_name}.\nEdit {commit_request['id']} has been committed"
    send_slack_message(message)

    print("Successfully executed the app bundle release to beta")


@task
def upload(c, ext):
    f = next(iter(Path("bin/").glob(f"*.{ext}")), None)
    print(f"Found: {f} for upload")
    if f:
        upload_to_site(f.as_posix())


@task
def build(c, env=os.environ):
    c.run(f"buildozer android debug", env=env).stdout
    c.run(f"buildozer android release", env=env).stdout


@task
def sign(
    c,
    release_path="/home/ubuntu/lnorb_com/orb-0.21.10-armeabi-v7a_arm64-v8a-release.aab",
    password=os.environ.get("KEYSTORE_PASS"),
):
    cert = (Path(os.getcwd()) / "lnorb_com.cer").as_posix()
    with Connection(
        "lnorb.com", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as con:
        keystore_path = "/home/ubuntu/keystores/com.orb.orb.keystore"
        aligned_path = Path(release_path).with_suffix(
            f".aligned{Path(release_path).suffix}"
        )
        con.run(
            f"jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -storepass {password} -keystore {keystore_path} {release_path} cb-play",
        )
        if con.run(f"test -f {aligned_path}", warn=True).ok:
            con.run(f"rm {aligned_path}")
        con.run(
            f"/home/ubuntu/.buildozer/android/platform/android-sdk/build-tools/33.0.0/zipalign -v 4 {release_path} {aligned_path}"
        )
        con.get(aligned_path, (Path(os.getcwd()) / aligned_path.name).as_posix())
        return aligned_path.name


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
                f"./build.py android.cython android.build --AWS-ACCESS-KEY-ID {env['AWS_ACCESS_KEY_ID']} --AWS-SECRET-ACCESS-KEY  {env['AWS_SECRET_ACCESS_KEY']}"
            )


@task
def cython(c, env=os.environ):
    for p in to_compile:
        p = Path(p)
        uid = "m" + sha256(p.as_posix().encode()).hexdigest()
        pyx = Path(f"lib/custom_lib/{uid}.pyx")
        py = Path(f"{str(p)}")
        with py.open() as pyf:
            pycontent = "\n".join(["# cython: language_level=3"] + pyf.readlines())
        write = False
        if pyx.exists():
            with pyx.open("r") as pyxf:
                pyxcontent = pyxf.read()
            if (
                sha256(pycontent.encode()).hexdigest()
                != sha256(pyxcontent.encode()).hexdigest()
            ):
                write = True
        else:
            write = True
        if write:
            with pyx.open("w") as pyxf:
                pyxf.write(pycontent)
        with pyx.open("w") as pyxf:
            pyxf.write(pycontent)
        with py.open("w") as pyf:
            pyf.write(f"from {uid} import *")


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
        "rsync -azv -e 'ssh -i lnorb_com.cer' . ubuntu@lnorb.com:/home/ubuntu/orb/ --exclude build --exclude dist --exclude .cache --exclude lnappstore/node_modules --exclude site/node_modules --exclude *.dmg --exclude setup.py --exclude *.so --exclude *.c",
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


def upload_to_s3(ext):
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
