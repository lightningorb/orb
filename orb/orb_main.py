# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-14 18:03:23
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-13 11:32:10

import sys

default_modules = set(sys.modules.keys())

import os

os.environ["KIVY_NO_ARGS"] = "1"

from traceback import format_exc
from pathlib import Path

from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore
from orb.core.orb_logging import get_logger

main_logger = get_logger(__name__)
debug = main_logger.debug

from kivy.config import Config
from kivy.utils import platform

if platform == "win":
    debug("windows detected, setting graphics multisampling to 0")
    Config.set("graphics", "multisamples", "0")

Config.set("graphics", "fullscreen", "0")
Config.write()

if platform == "macosx":
    os.environ["KIVY_DPI"] = "240"
    os.environ["KIVY_METRICS_DENSITY"] = "1.5"

from orb.core_ui.app_common import AppCommon

debug("importing orb modules")


error = ""


from orb.connector.orb_connector_app import OrbConnectorApp
from orb.misc.monkey_patch import do_monkey_patching


class OrbCrashWrapper(AppCommon):
    def __init__(self, text):
        self.text = text
        super(OrbCrashWrapper, self).__init__()

    def build(self):
        self.text_input = TextInput(text=self.text)
        self.store = JsonStore(
            Path(self._get_user_data_dir()) / "orb_crash_wrapper.json"
        )
        return self.text_input


def main():
    do_monkey_patching()
    from kivy.config import ConfigParser

    use_crash_wrapper = True
    config = ConfigParser()
    os.makedirs(OrbConnectorApp()._get_user_data_dir(), exist_ok=True)
    config_path = Path(OrbConnectorApp()._get_user_data_dir()) / "orbconnector.ini"
    if not config_path.exists():
        with config_path.open("w") as f:
            f.write("")
    config.read(config_path.as_posix())
    for section in ["host", "ln"]:
        try:
            config.add_section(section)
        except:
            pass
    try:
        pk = config.get("ln", "identity_pubkey", fallback="")
        if not pk:
            app = OrbConnectorApp()
            app.run()
            sys.exit(0)
        else:
            from orb.core_ui.orb_app import OrbApp

            OrbApp.__name__ = f"Orb_{pk}"
            OrbApp().run(config)
    except Exception as e:
        print(e)
        print(format_exc())
        if use_crash_wrapper:
            text = str(e)
            text += "\n"
            text += format_exc()
            app_crash_wrapper = OrbCrashWrapper(text)
            app_crash_wrapper.run()
