# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-06 21:07:13

from threading import Thread
from orb.store.scripts import scripts, Script, save_scripts
from textwrap import dedent
import os


class Plugin:
    def install(self, script_name, menu, uuid):
        menu = ">".join(x.strip() for x in menu.split(">"))
        sc, ext = os.path.splitext(script_name)
        code = dedent(
            f"""
            import {sc}
            from importlib import reload
            reload({sc})
            {sc}.main()
            """
        )
        scripts[uuid] = Script(code=code, menu=menu, uuid=uuid)
        save_scripts()
