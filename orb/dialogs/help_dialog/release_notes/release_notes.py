# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-14 06:52:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-14 07:25:02

from orb.components.popup_drop_shadow import PopupDropShadow
from pathlib import PurePath


class ReleaseNotes(PopupDropShadow):
    def open(self, *args):
        path = PurePath(__file__).parent / "release_notes.txt"
        self.ids.release_notes.text = open(path).read()
        super(ReleaseNotes, self).open(self, *args)
