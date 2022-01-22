# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-18 17:03:03
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-22 14:55:16

from invoke import task
import os

# ./build.py -H ubuntu@18.118.53.220 -i orbdb.cer appstore.remote.clone
# ./build.py -H ubuntu@18.118.53.220 -i orbdb.cer appstore.remote.install-service
# ./build.py -H ubuntu@18.118.53.220 -i orbdb.cer appstore.remote.drop-tables


@task
def start(c, env=os.environ["PATH"]):
    uvcpath = "/Library/Frameworks/Python.framework/Versions/3.9/bin/uvicorn"
    with c.cd("server"):
        c.run(f"{uvcpath} orb_server:app --reload")


@task
def create_db(c, env=os.environ["PATH"]):
    c.run("sudo -u postgres createdb orb")


@task
def install_stack(c):
    c.run("uname -a")
    c.sudo("apt-get update -y")
    c.sudo(
        "apt-get install nginx supervisor git postgresql postgresql-contrib python3-pip -y"
    )


@task
def clone(c):
    if c.run("test -d orb", warn=True).failed:
        c.run(
            f"git clone https://{open('.gittoken').read().strip()}@github.com/bc31164b-cfd5-4a63-8144-875100622b2d/orb.git"
        )
    with c.cd("orb"):
        c.run("git pull")
        c.run("git checkout appstore3")


@task
def requirements(c):
    with c.cd("orb/server"):
        c.run("python3 -m pip install -r requirements.txt")


@task
def create_user(c):
    c.run("sudo -u postgres createuser --interactive --pwprompt")


@task
def create_tables(c):
    with c.cd("orb/server"):
        c.run("python3 create_db.py")


@task
def drop_tables(c):
    with c.cd("orb/server"):
        c.run("python3 drop_db.py")


@task
def start_dev(c):
    with c.cd("orb/server"):
        c.run(f"/home/ubuntu/.local/bin/uvicorn orb_server:app --reload --host 0.0.0.0")


@task
def install_service(c):
    if c.run("test -d /etc/supervisor/conf.d/orb.conf", warn=True).failed:
        c.put("build_system/appstore/orb.conf", "/tmp/")
        c.sudo("mv /tmp/orb.conf /etc/supervisor/conf.d/")
    c.sudo("supervisorctl reread")
    c.sudo("supervisorctl update")


@task
def install_nginx_conf(c):
    c.put("build_system/appstore/orb_nginx.conf", "/tmp/")
    c.sudo("mv /tmp/orb_nginx.conf /etc/nginx/sites-available/")
    c.sudo(
        "ln /etc/nginx/sites-available/orb_nginx.conf /etc/nginx/sites-enabled/orb_nginx.conf -sf"
    )
    c.sudo("nginx -s reload")


@task
def certbot(c):
    c.sudo("pip3 install pip --upgrade")
    c.sudo("pip3 install certbot certbot-nginx")
    c.sudo("certbot --nginx -d lnappstore.com")
