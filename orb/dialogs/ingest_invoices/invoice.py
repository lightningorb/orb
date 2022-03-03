# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-03-04 03:01:35
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-03-04 03:05:23

import arrow

from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

class Invoice(BoxLayout):
    raw = ObjectProperty("")
    destination = ObjectProperty("")
    num_satoshis = ObjectProperty(0)
    timestamp = ObjectProperty(0)
    expiry = ObjectProperty(0)
    description = ObjectProperty("")
    paid = BooleanProperty(False)
    id = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(Invoice, self).__init__(*args, **kwargs)

        self.schedule = Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        delta = int(self.timestamp) + int(self.expiry) - int(arrow.utcnow().timestamp())
        if delta < 0:
            self.ids.expiry_label.text = "expired"
        else:
            self.ids.expiry_label.text = (
                arrow.utcnow()
                .shift(seconds=delta)
                .humanize(granularity=["hour", "minute", "second"])
            )

    def dismiss(self):
        Clock.unschedule(self.schedule)
