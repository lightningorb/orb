# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-11 16:54:10
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-11 17:30:38

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc import data_manager


class HighlighterDialog(PopupDropShadow):
    def open(self):
        super(HighlighterDialog, self).open()
        h = data_manager.data_man.store.get("highlighter", {})
        self.ids.text_input.text = h.get("highlight", "")

    def validate(self, text):
        h = data_manager.data_man.store.get("highlighter", {})
        h["highlight"] = text
        data_manager.data_man.store.put("highlighter", **h)
        data_manager.data_man.highlighter_updated += 1
