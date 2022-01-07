# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:31:00
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-07 08:25:01

from kivy.app import App
from orb.misc.plugin import Plugin


class ToggleSentRecieved(Plugin):
    def main(self):
        show = self.app.config["display"]["show_sent_received"]
        self.app.config["display"]["show_sent_received"] = "10"[show == "1"]
        self.get_screen("channels").refresh()

    @property
    def menu(self):
        return "UI > toggle sent / received"

    @property
    def uuid(self):
        return "78921c3b-5b78-49d9-9e0e-2aed2cc64b9e"
