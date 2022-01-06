# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 19:26:18
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-06 22:45:53

import yaml
import os
from kivy.app import App

scripts = {}


class Script:
    def __init__(self, code, menu, uuid):
        self.code = code
        self.menu = menu
        self.uuid = uuid


def get_loader():
    loader = yaml.SafeLoader
    loader.add_constructor("!Script", lambda l, n: Script(**l.construct_mapping(n)))
    return loader


def get_dumper():
    safe_dumper = yaml.SafeDumper
    safe_dumper.add_representer(
        Script,
        lambda dumper, inst: dumper.represent_mapping(
            "!Script",
            {
                "menu": inst.menu,
                "code": inst.code,
                "uuid": inst.uuid,
            },
        ),
    )
    return safe_dumper


def load_scripts():
    load = (
        lambda x: yaml.load(open(x, "r"), Loader=get_loader())
        if os.path.exists(x)
        else {}
    )
    scripts.clear()
    user_data_dir = App.get_running_app().user_data_dir
    scripts.update(load(os.path.join(user_data_dir, "scripts.yaml")))
    return scripts


def save_scripts():
    user_data_dir = App.get_running_app().user_data_dir

    with open(os.path.join(user_data_dir, "scripts.yaml"), "w") as stream:
        stream.write(yaml.dump(scripts, Dumper=get_dumper()))


if __name__ == "__main__":
    scripts.update(Script(code='print("Hello World")', menu="test > hello world"))
    save_scripts()
    print(load_scripts())
