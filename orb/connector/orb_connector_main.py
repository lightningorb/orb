# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-29 12:16:37
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-01 11:35:35

from pathlib import Path

from kivymd.uix.screen import MDScreen
from kivy.app import App
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp


class OrbConnectorMain(MDScreen):
    def add_released(self, button):
        if button.icon == "alpha-u-circle-outline":
            App.get_running_app().screen.ids.sm.current = "umbrel_node"
            self.manager.transition.direction = "left"
        elif button.icon == "lightning-bolt-outline":
            App.get_running_app().screen.ids.sm.current = "voltage_node"
            self.manager.transition.direction = "left"
        elif button.icon == "wizard-hat":
            App.get_running_app().screen.ids.sm.current = "ssh_wizard"
            self.manager.transition.direction = "left"
        elif button.icon == "cogs":
            App.get_running_app().screen.ids.sm.current = "connection_settings"
            self.manager.transition.direction = "left"
        elif button.icon == "export":
            App.get_running_app().screen.ids.sm.current = "export_node_settings"
            self.manager.transition.direction = "left"
        elif button.icon == "import":
            App.get_running_app().screen.ids.sm.current = "import_node_settings"
            self.manager.transition.direction = "left"
