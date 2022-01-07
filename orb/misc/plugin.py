# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-07 09:42:50

from textwrap import dedent
from threading import Thread
import os

from orb.store.scripts import scripts, Script, save_scripts

from kivy.app import App


class Plugin:
    def install(self, script_name, class_name):
        menu = ">".join(x.strip() for x in self.menu.split(">")) if self.menu else None
        sc, ext = os.path.splitext(os.path.basename(script_name))
        code = dedent(
            f"""
            import {sc}
            from importlib import reload
            reload({sc})
            {sc}.{class_name}().main()
            """
        )
        scripts[self.uuid] = Script(code=code, menu=menu, uuid=self.uuid)
        save_scripts()

    @property
    def app(self):
        return App.get_running_app()

    def get_screen(self, name):
        return app.root.ids.sm.get_screen(name)

    @property
    def menu(self):
        return None
