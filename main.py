# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-26 17:57:48
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-02 23:49:59

import sys

default_modules = set(sys.modules.keys())

import os
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


if __name__ == "__main__":
    debug("in __main__")
    debug("launching main Orb App")
    do_monkey_patching()
    try:
        debug("creating orb connector app")
        app = OrbConnectorApp()
        debug("running orb connector app")
        app.run()
        debug("done running orb connector app")
        node_settings = copy(app.node_settings)
        debug("clearing widgets")
        app.root.ids.sm.clear_widgets()
        debug("deleting app")
        del app
        import gc

        debug("garbage collecting")
        gc.collect()
        debug("loading orb app")

        from orb.core_ui.orb_app import OrbApp

        debug("getting id pubkey")

        if node_settings.get("lnd.identity_pubkey"):
            OrbApp.__name__ = f"Orb_{node_settings['lnd.identity_pubkey']}"
            debug("running orb app")
            OrbApp().run(node_settings)
    except Exception as e:
        print(e)
        text = str(e)
        text += "\n"
        text += format_exc()
        app_crash_wrapper = OrbCrashWrapper(text)
        app_crash_wrapper.run()
