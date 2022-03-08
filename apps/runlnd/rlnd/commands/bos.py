import os
from invoke import task
from .utils import get_conf_file_path


@task
def install(c):
    """
    Install Balance of Satohis. Includes first installing and configuring nodejs.
    """
    c.run("curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -")
    c.sudo("apt-get install -y build-essential")
    c.sudo("apt-get install -y nodejs")
    c.run("mkdir -p ~/.npm-global")
    c.run('npm config set prefix "~/.npm-global"')
    c.run("npm i -g balanceofsatoshis")
    c.run(
        '(crontab -l 2>/dev/null; echo "*/5 * * * * /home/ubuntu/.npm-global/bin/bos unlock /home/ubuntu/.lnd/wallet_password") | crontab -'
    )


@task
def unlock(c):
    """
    Unlock lightning wallet using bos.
    """
    c.run("bos unlock /home/ubuntu/.lnd/wallet_password")


@task
def install_tg_bot(c):
    """
    Install, configure, enable and start bos telegram bot.
    """
    connection_code = input("Telegram connection code: ").strip()
    conf = (
        open(get_conf_file_path("bostg.service"))
        .read()
        .replace("{connection_code}", connection_code)
    )
    with open("bostg.service", "w") as f:
        f.write(conf)
    c.put("bostg.service", "/tmp/bostg.service")
    os.unlink("bostg.service")
    c.sudo("mv /tmp/bostg.service /etc/systemd/system/bostg.service")
    c.sudo("systemctl enable bostg")
    c.sudo("systemctl start bostg")


@task
def tunnel_gateway(c):
    """
    Bos has some basic UI functionality, however it doesn't do much besides
    allowing to send and recieve lightning payments. To try it out, run:

    rln -- bos gateway

    in a second terminal run:

    rln bos.tunnel-gateway

    then head to: https://ln-operator.github.io/ and paste the connect code you were
    provided with in the first terminal
    """
    c.local(
        f"ssh -i {c.connect_kwargs['key_filename'][0]} -L 4805:{c.host}:4805 {c.user}@{c.host}"
    )
