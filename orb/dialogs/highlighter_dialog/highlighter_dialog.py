# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-11 16:54:10
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-06 10:24:52

from kivy.app import App


from orb.components.popup_drop_shadow import PopupDropShadow


class HighlighterDialog(PopupDropShadow):
    def open(self):
        super(HighlighterDialog, self).open()
        h = App.get_running_app().store.get("highlighter", {})
        self.ids.text_input.text = h.get("highlight", "")

    def validate(self, text):
        app = App.get_running_app()
        h = app.store.get("highlighter", {})
        h["highlight"] = text
        app.store.put("highlighter", **h)
        app.highlighter_updated += 1
