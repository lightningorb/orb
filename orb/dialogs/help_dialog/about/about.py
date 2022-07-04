# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-26 18:25:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-04 11:32:33

from pathlib import Path
from kivy.app import App

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.get_platform_name import *
from traceback import format_exc


class About(PopupDropShadow):
    def open(self, *args):
        version = App.get_running_app().version
        text = f"Orb v{version}\n\n"
        try:
            text += 'platform.system is "%s"\n' % platform.system()
        except Exception as e:
            print(e)
            print(format_exc())
        try:
            text += 'platform.machine is "%s"\n' % platform.machine()
        except Exception as e:
            print(e)
            print(format_exc())
        try:
            text += 'sys.byteorder is "%s"\n' % sys.byteorder
        except Exception as e:
            print(e)
            print(format_exc())
        try:
            text += 'The standard platform name is "%s"\n\n' % format_platform()
        except Exception as e:
            print(e)
            print(format_exc())
        text += "Orb is being developed in the\nheart of the plebnet.\n\nBig thanks to:\n\nMiguel\nRichard\nMads\nAsher\n\nAnd countless others for their\ntime, input and knowledge."
        self.ids.label.text = text
        super(About, self).open()
