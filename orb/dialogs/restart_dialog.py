# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-22 05:36:17
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-02 16:33:01


from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.app import App


class RestartDialog(MDDialog):
    def __init__(
        self, title="Please click 'Quit' and restart Orb to use connector", buttons=None
    ):
        if not buttons:
            buttons = [
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    # text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dismiss(),
                ),
                MDFlatButton(
                    text="Quit",
                    theme_text_color="Custom",
                    # text_color=self.theme_cls.primary_color,
                    on_release=lambda x: App.get_running_app().stop(),
                ),
            ]
        super(RestartDialog, self).__init__(title=title, buttons=buttons)
