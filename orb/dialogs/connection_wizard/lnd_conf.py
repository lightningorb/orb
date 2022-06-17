# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 09:17:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-17 08:34:57

from threading import Thread
from pathlib import Path
import re
import configparser
from tempfile import gettempdir
import time

from orb.misc.decorators import guarded
from orb.dialogs.connection_wizard.tab import Tab
from orb.misc.utils import pref
from orb.misc.fab_factory import Connection
from orb.lnd.lnd_conf import LNDConf as LNDConfParser

from kivy.uix.textinput import TextInput


class FocusTextInput(TextInput):
    def on_touch_down(self, touch):
        from orb.misc import data_manager

        if self.collide_point(*touch.pos):
            if data_manager.data_man.menu_visible:
                return False
        return super(FocusTextInput, self).on_touch_down(touch)


class LNDConf(Tab):
    @guarded
    def check_lnd_conf(self):
        with Connection() as c:
            lnd_conf = c.run(f'cat {pref("lnd.conf_path")}', hide=True).stdout
            self.config = LNDConfParser()
            self.config.read_string(lnd_conf)
            app_options = self.config.get_section("[Application Options]")
            tlsextraips = app_options.get("tlsextraip")
            tlsextradomains = app_options.get("tlsextradomain")
            hostname = pref("host.hostname")
            changes = []
            is_ip = re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", hostname)
            if is_ip:
                if hostname not in tlsextraips:
                    app_options.add("tlsextraip", hostname)
                    changes.append("tlsextraip modified")
            else:
                if hostname not in tlsextradomains:
                    app_options.add("tlsextradomain", hostname)
                    changes.append("tlsextradomain modified")
            if "1" not in app_options.get("tlsautorefresh"):
                changes.append("tlsautorefresh modified")
                app_options.set("tlsautorefresh", "1")
            if "0.0.0.0:10009" not in app_options.get("rpclisten"):
                changes.append("rpclisten modified")
                app_options.set("rpclisten", "0.0.0.0:10009")
            if "0.0.0.0:8080" not in app_options.get("restlisten"):
                changes.append("restlisten modified")
                app_options.set("restlisten", "0.0.0.0:8080")
            self.ids.input.text = self.config.to_string()
            self.ids.report.text = "\n".join(
                changes if changes else ["no changes required"]
            )

    @guarded
    def modify_lnd_conf(self):
        with Connection() as c:
            epoch_time = int(time.time())
            backup = f'{pref("lnd.conf_path")}.{epoch_time}.backup'
            print(f"Creating lnd.conf backup {backup}")
            c.run(
                f'cp {pref("lnd.conf_path")} {backup}',
                hide=True,
            )
            path = (Path(f"{gettempdir()}") / "lnd.conf").as_posix()
            print(path, pref("lnd.conf_path"))
            # c.put(path, pref("lnd.conf_path"))
