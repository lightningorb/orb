import re

from tempfile import NamedTemporaryFile
from invoke import task
from .utils import get_conf_file_path


def subst_conf_strings(conf):
    regex = r"(^[\da-z A-Z\.-]*\s*)=(\s*.*)"
    subst = "lnd.\\1=\\2"
    return re.sub(regex, subst, conf, 0, re.MULTILINE)


def subst_headers(conf):
    regex = r"(\[[^\]]+\])"
    subst = "# \\1"
    return re.sub(regex, subst, conf, 0, re.MULTILINE)


def configure(c):
    c.run("mkdir -p .lit")
    lndc = c.run("cat .lnd/lnd.conf", hide=True).stdout
    lndc = subst_conf_strings(lndc)
    lndc = subst_headers(lndc)

    litc = open(get_conf_file_path("lit.conf")).read()
    litc = litc.replace("{lndc}", lndc)
    open("lit.conf", "w").write(litc)

    tf = NamedTemporaryFile(mode="w")
    tf.write(litc)
    tf.flush()
    c.put(tf.name, ".lit/lit.conf")
    tf.close()


def open_firewall(c):
    c.run("ufw allow 443")


def download_and_install(c):
    c.run("rm -rf src/lit")
    c.run("mkdir -p src/lit")
    with c.cd("src/lit"):
        c.run(
            "wget https://github.com/lightninglabs/lightning-terminal/releases/download/v0.5.0-alpha/lightning-terminal-linux-amd64-v0.5.0-alpha.tar.gz"
        )
        c.run("tar xvf lightning-terminal-linux-amd64-v0.5.0-alpha.tar.gz")
        for b in ["litd", "frcli", "loop", "pool", "lncli"]:
            c.run(f"cp lightning-terminal-linux-amd64-v0.5.0-alpha/{b} $GOPATH/bin/")
        c.run("sudo setcap 'CAP_NET_BIND_SERVICE=+eip' $GOPATH/bin/litd")


def install_service(c):
    if c.run("test -d /etc/systemd/system/lit.service", warn=True).failed:
        c.put(get_conf_file_path("lit.service"), "/tmp/lit.service")
        c.sudo("mv /tmp/lit.service /etc/systemd/system/lit.service")
        c.sudo("systemctl daemon-reload")


@task
def install(c):
    # configure(c)
    # download_and_install(c)
    install_service(c)


@task
def start(c):
    c.sudo("systemctl start lit")


@task
def stop(c):
    c.sudo("systemctl stop lit")


@task
def journal(c):
    c.sudo("journalctl -u lit.service")
