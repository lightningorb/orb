# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-26 18:25:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-04-02 10:08:15

from pathlib import Path
from kivy.app import App

from orb.components.popup_drop_shadow import PopupDropShadow


class About(PopupDropShadow):
    def open(self, *args):
        version = App.get_running_app().version
        text = f"Orb v{version}\n\n"
        text += "Orb is being developed in the\nheart of the plebnet.\n\nBig thanks to:\n\nMiguel\nRichard\nMads\nAsher\n\nAnd countless others for their\ntime, input and knowledge."
        self.ids.label.text = text
        super(About, self).open()
