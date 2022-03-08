import os
import shutil
import toml
from invoke import task
from textwrap import dedent


config_dir = os.path.expanduser("~/.rln")
if not os.path.isdir(config_dir):
    os.mkdir(config_dir)

prefs_file = os.path.join(config_dir, "prefs.toml")


def config_node_dir(name):
    dir_path = os.path.join(config_dir, name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    return dir_path


def get_default():
    if os.path.exists(prefs_file):
        with open(prefs_file) as f:
            prefs = toml.load(f)
    return prefs["node"]["default"]


get_key_path = lambda name: os.path.join(config_node_dir(name), f"{name}.pem")
get_secrets_path = lambda name: os.path.join(
    config_node_dir(name), f"{name}_secrets.zip"
)


@task
def save(c, name):
    """
    Save the current connection into ~/.rln/prefs.toml.
    This becomes the default configuration for rln,
    so the host no longer needs to be explicitely
    detailed upon invocation.

    e.g

    $ rln -H ubuntu@10.10.10.10 -i ~/.rln/lightning/lightning_key.pem prefs.save lightning
    $ rln -H ubuntu@20.20.20.20 -i ~/.rln/testnet/testnet_key.pem prefs.save testnet
    """
    prefs = {"node": {"default": ""}}
    if os.path.exists(prefs_file):
        with open(prefs_file) as f:
            prefs = toml.load(f)
    prefs["node"]["default"] = name
    if name not in prefs["node"]:
        prefs["node"][name] = {}
    prefs["node"][name]["host"] = c.host
    prefs["node"][name]["user"] = c.user
    prefs["node"][name]["name"] = name
    if os.path.exists(get_key_path(name)):
        prefs["node"][name]["keyfile"] = get_key_path(name)
    with open(prefs_file, "w") as f:
        toml.dump(prefs, f)


@task
def set_default(c, name):
    """
    Set the default (preferred) node for future CLI commands.
    The name of the node needs to exist in your prefs file.

    e.g:

    $ rln prefs.set-default lightning
    $ rln -- uname -a

    output:

    Linux ip-x-x-x-x 5.8.0-1038-aws #40~20.04.1-Ubuntu SMP Thu Jun 17 13:25:28 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux

    $ rln prefs.set-default testnet
    $ rln -- uname -a

    output:

    Linux testnet 5.8.0-55-generic #62-Ubuntu SMP Tue Jun 1 08:21:18 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
    """
    if os.path.exists(prefs_file):
        with open(prefs_file) as f:
            prefs = toml.load(f)
    prefs["node"]["default"] = name
    with open(prefs_file, "w") as f:
        toml.dump(prefs, f)


@task
def show_default(c):
    """
    Show the default (preferred) node for future CLI commands.
    """
    if os.path.exists(prefs_file):
        with open(prefs_file) as f:
            prefs = toml.load(f)
    print(prefs["node"]["default"])
    print(prefs["node"][prefs["node"]["default"]])


@task
def show(c):
    """
    Show prefs file.
    """
    print(prefs_file)
    if os.path.exists(prefs_file):
        with open(prefs_file) as f:
            prefs = toml.load(f)
            print(prefs)


@task
def remove(c, name):
    """
    Remove node from prefs file, and delete its .pem and secrets
    """
    if os.path.exists(prefs_file):
        with open(prefs_file) as f:
            prefs = toml.load(f)
    if name == prefs["node"]["default"]:
        prefs["node"]["default"] = ""
    if prefs["node"].get(name):
        del prefs["node"][name]
    with open(prefs_file, "w") as f:
        toml.dump(prefs, f)
    cdir = config_node_dir(name)
    # be careful as we're about to delete stuff
    assert cdir.startswith(os.path.expanduser("~/.rln"))
    assert name in cdir
    shutil.rmtree(cdir)


@task
def reset_prefs_file(c):
    """
    Delete the prefs file.
    """
    if os.path.exists(prefs_file):
        os.unlink(prefs_file)


def load():
    """
    Read preferred connection information.
    """
    with open(f"{config_dir}/prefs.toml", "r") as f:
        return toml.loads(f.read())
