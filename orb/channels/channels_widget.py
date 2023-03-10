# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-24 08:56:07

from time import time

from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
from kivy.properties import NumericProperty
from kivy.app import App


from orb.ln import Ln
from orb.misc.utils import pref
from orb.widgets.node import Node
from orb.misc.prefs import is_mock
from orb.misc.utils import prefs_col
from orb.misc.decorators import guarded
from orb.channels.CN_widget import CNWidget
from orb.misc.enums import ChannelsWidgetUXMode
from orb.widgets.chord_widget import ChordWidget
from orb.channels.channels_thread import ChannelsThread


class ChannelsWidget(ScatterLayout):
    mode = NumericProperty(0)

    @guarded
    def __init__(self, gestures_delegate, *args, **kwargs):
        super(ChannelsWidget, self).__init__(*args, **kwargs)

        # importing model related things before the tables are created
        # is not allowed, which is why this is imported here
        from orb.logic.htlcs_thread import HTLCsThread
        from orb.logic.invoices_thread import InvoicesThread

        app = App.get_running_app()

        self.htlcs_thread = HTLCsThread(inst=self, name="HTLCsThread")
        self.htlcs_thread.daemon = True
        self.invoices_thread = InvoicesThread(inst=self, name="InvoicesThread")
        self.invoices_thread.daemon = True
        self.node = None
        self.channels = app.channels
        if self.channels:
            self.channels.get()
        self.channels_thread = ChannelsThread(inst=self, name="ChannelsThread")
        self.channels_thread.daemon = True
        self.cn = {}
        self.touch_time = time()
        self.gestures_delegate = gestures_delegate
        self.mode = app.channels_widget_ux_mode

        def update_mode(_, val):
            self.mode = val

        app.bind(channels_widget_ux_mode=update_mode)
        self.ln = Ln(node_type=pref("host.type"))
        self.chord_widget = ChordWidget(self.channels)
        caps = self.get_caps(self.channels)
        self.info = self.ln.get_info()
        if self.channels:
            for c in self.channels:
                self.add_channel(channel=c, caps=caps, update=False)
        self.node = Node(
            text=self.info.alias,
            round=pref("display.round_central_node"),
        )
        self.ids.relative_layout.add_widget(self.node)
        self.ids.relative_layout.add_widget(self.chord_widget)
        self.bind(size=self.update)
        App.get_running_app().bind(update_channels_widget=self.update)
        self.apply_transform(
            Matrix().scale(0.3, 0.3, 0.3), anchor=(self.size[0] / 2, self.size[1] / 2)
        )

        if not is_mock():
            if pref("host.type") == "lnd":
                self.htlcs_thread.start()
                self.invoices_thread.start()
                self.channels_thread.start()
            elif pref("host.type") == "cln":
                try:
                    wss_hostname = pref("c-lightning-events.hostname")
                    if wss_hostname:
                        self.htlcs_thread.start()
                except:
                    pass

#        self.gestures_delegate.init_gdb(self)

    def add_channel(self, channel, caps=None, update=True):
        if not caps:
            caps = self.get_caps(self.channels)
        cn = CNWidget(c=channel, caps=caps)
        self.cn[channel.chan_id] = cn
        self.ids.relative_layout.add_widget(cn)
        if update:
            self.update()

    def remove_channel(self, channel, caps=None):
        self.ids.relative_layout.remove_widget(self.cn[channel.chan_id])
        del self.cn[channel.chan_id]

    def get_caps(self, channels):
        if not channels:
            return 1
        max_cap = max([int(c.capacity) for c in channels])
        return {c.chan_id: max(2, int(int(c.capacity) / max_cap) * 5) for c in channels}

    def update(self, *_):
        if self.node:
            self.node.pos = (-(self.node.width_pref / 2), -(self.node.height_pref / 2))
        if self.channels:
            self.channels.sort_channels()
            do_update = False
            for i, chan_id in enumerate(self.channels.sorted_chan_ids):
                keys = [*self.cn.keys()]
                if chan_id in keys:
                    self.cn[chan_id].update(i, len(self.cn))
                else:
                    print(chan_id, 'not in', keys)
                    print(f"Channel {chan_id} not found in channels_widget")
                    self.add_channel(self.channels.channels[chan_id], update=False)
            if do_update:
                self.update()

    def on_touch_move(self, touch):
        app = App.get_running_app()
        if app.menu_visible:
            return False
        if self.mode == ChannelsWidgetUXMode.gestures:
            self.gestures_delegate.on_touch_move(touch)
            return False
        return super(ChannelsWidget, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.mode == ChannelsWidgetUXMode.gestures:
            self.gestures_delegate.on_touch_up(touch)
            return False
        return super(ChannelsWidget, self).on_touch_up(touch)

    def on_touch_down(self, touch):
        """
        Touch down event in the channels widget.
        """
        app = App.get_running_app()
        if app.menu_visible:
            return False
        if self.mode == ChannelsWidgetUXMode.gestures:
            self.gestures_delegate.on_touch_down(touch)
            return False
        if touch.is_mouse_scrolling:
            scroll_delta = 0.2
            s = dict(scrolldown=1 + scroll_delta, scrollup=1 - scroll_delta).get(
                touch.button
            )
            if s:
                self.apply_transform(Matrix().scale(s, s, s), anchor=touch.pos)
        else:
            App.get_running_app().selection = None
            if self.node:
                self.node.col = prefs_col("display.node_background_color")
        super(ChannelsWidget, self).on_touch_down(touch)
