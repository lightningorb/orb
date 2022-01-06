# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:31:00
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-06 20:33:15

from kivy.app import App
from orb.misc.plugin import Plugin


Plugin().install(
    script_name="toggle_sent_received.py",
    menu="UI > toggle sent / received",
    uuid="78921c3b-5b78-49d9-9e0e-2aed2cc64b9e",
)


def main():
    app = App.get_running_app()
    show = app.config["display"]["show_sent_received"]
    app.config["display"]["show_sent_received"] = "10"[show == "1"]
    app.root.ids.sm.get_screen("channels").refresh()
