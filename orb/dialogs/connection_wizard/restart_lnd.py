# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 09:17:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-17 08:33:57

from threading import Thread
from pathlib import Path
import re
import configparser
from tempfile import gettempdir
from kivy.clock import mainthread
import time

from orb.misc.decorators import guarded
from orb.dialogs.connection_wizard.tab import Tab
from orb.misc.utils import pref
from orb.misc.fab_factory import Connection

from kivy.uix.textinput import TextInput


class FocusTextInput(TextInput):
    def on_touch_down(self, touch):
        from orb.misc import data_manager

        if self.collide_point(*touch.pos):
            if data_manager.data_man.menu_visible:
                return False
        return super(FocusTextInput, self).on_touch_down(touch)


class RestartLND(Tab):
    def __init__(self, *args, **kwargs):
        super(RestartLND, self).__init__(*args, **kwargs)
        self.log_proc = None

    def stream_log(self):
        def func():
            class Out:
                @mainthread
                def write(_, b):
                    if b and b != "\n":
                        lines = self.ids.input.text.split("\n") + [
                            x for x in b.split("\n") if x != "\n"
                        ]
                        self.ids.input.text = "\n".join(lines[len(lines) - 30 :])

                def flush(self):
                    pass

            with Connection() as c:
                if not self.log_proc or (
                    self.log_proc and not self.log_proc.ok or self.log_proc.exited
                ):
                    self.log_proc = c.run(
                        f"tail -f {pref('lnd.log_path')}",
                        hide=True,
                        out_stream=Out(),
                        asynchronous=True,
                    )
                    self.log_proc.exited = False
                    self.log_proc.join()

        Thread(target=func).start()

    @guarded
    def restart_lnd(self):
        with Connection() as c:
            c.sudo(pref("lnd.stop_cmd"))
            c.sudo(pref("lnd.start_cmd"))
