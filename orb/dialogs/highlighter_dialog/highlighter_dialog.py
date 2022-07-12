# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-11 16:54:10
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-01 11:21:56

from kivy.app import App

from orb.misc import data_manager
from orb.components.popup_drop_shadow import PopupDropShadow


class HighlighterDialog(PopupDropShadow):
    def open(self):
        super(HighlighterDialog, self).open()
        h = App.get_running_app().store.get("highlighter", {})
        self.ids.text_input.text = h.get("highlight", "")

    def validate(self, text):
        h = App.get_running_app().store.get("highlighter", {})
        h["highlight"] = text
        App.get_running_app().store.put("highlighter", **h)
        data_manager.data_man.highlighter_updated += 1
