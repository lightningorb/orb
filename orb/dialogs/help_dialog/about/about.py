# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-26 18:25:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-04-02 08:39:16
from orb.components.popup_drop_shadow import PopupDropShadow


class About(PopupDropShadow):
    def open(self, *args):
        self.ids.label.text = "Orb is being developed in the\nheart of the plebnet.\n\nBig thanks to:\n\nMiguel\nRichard\nMads\nAsher\n\nAnd countless others for their\ntime, input and knowledge."
        super(About, self).open()
