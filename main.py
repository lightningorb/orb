# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-26 17:57:48
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-04 13:25:59

import sys

default_modules = set(sys.modules.keys())

import os

os.environ["KIVY_NO_ARGS"] = "1"

from copy import copy
from traceback import format_exc
from pathlib import Path

from kivy.uix.textinput import TextInput
from orb.core.logging import get_logger
from kivy.app import App

main_logger = get_logger(__name__)
debug = main_logger.debug

from kivy.config import Config
from kivy.utils import platform

if platform == "win":
    debug("windows detected, setting graphics multisampling to 0")
    Config.set("graphics", "multisamples", "0")

if platform == "macosx":
    os.environ["KIVY_DPI"] = "240"
    os.environ["KIVY_METRICS_DENSITY"] = "1.5"

from orb.core_ui.app_common import AppCommon
from orb.misc.utils import get_available_nodes
import argparse


debug("appending paths to include lnd and third party modules")
parent_dir = Path(__file__).parent
sys.path.append((parent_dir / Path("orb/lnd")).as_posix())
sys.path.append((parent_dir / Path("orb/lnd/grpc_generated")).as_posix())
sys.path.append((parent_dir / Path("third_party/contextmenu")).as_posix())
sys.path.append((parent_dir / Path("third_party/arrow")).as_posix())
sys.path.append((parent_dir / Path("third_party/python-qrcode/")).as_posix())
sys.path.append((parent_dir / Path("third_party/forex-python/")).as_posix())
sys.path.append((parent_dir / Path("third_party/bezier/src/python/")).as_posix())
sys.path.append((parent_dir / Path("third_party/colour/")).as_posix())
sys.path.append((parent_dir / Path("third_party/currency-symbols/")).as_posix())

debug("importing orb modules")

from orb.core_ui.hidden_imports import *


error = ""


from orb.dialogs.umbrel_node.umbrel_node import UmbrelNode
from orb.dialogs.voltage_node.voltage_node import VoltageNode
from orb.orb_connector_main import OrbConnectorMain
from orb.orb_connector_app import OrbConnectorApp
from orb.misc.monkey_patch import do_monkey_patching


class OrbCrashWrapper(AppCommon):
    def __init__(self, text):
        self.text = text
        super(OrbCrashWrapper, self).__init__()

    def build(self):
        self.text_input = TextInput(text=self.text)
        return self.text_input


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pubkey", help="specify pubkey of node to load", required=False
    )
    args = parser.parse_args()
    return args


def get_pubkey(settings_pubkey, args_pubkey):
    if settings_pubkey:
        return settings_pubkey
    elif args_pubkey:
        return next(
            iter(x for x in get_available_nodes() if x.startswith(args_pubkey)), None
        )


if __name__ == "__main__":
    do_monkey_patching()
    args = parse_args()
    node_settings = {}
    try:
        if not args.pubkey:
            app = OrbConnectorApp()
            app.run()
            node_settings = copy(app.node_settings)
            app.root.ids.sm.clear_widgets()
            del app
            import gc

            gc.collect()

        from orb.core_ui.orb_app import OrbApp

        pk = get_pubkey(node_settings.get("lnd.identity_pubkey"), args.pubkey)

        if pk:
            OrbApp.__name__ = f"Orb_{pk}"
            OrbApp().run(node_settings)
    except Exception as e:
        print(e)
        text = str(e)
        text += "\n"
        text += format_exc()
        app_crash_wrapper = OrbCrashWrapper(text)
        app_crash_wrapper.run()
