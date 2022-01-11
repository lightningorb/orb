# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-11 06:55:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-11 13:19:06

from kivy.graphics import Line, Ellipse, Color
from kivy.gesture import Gesture, GestureDatabase
import data_manager

from orb.logic.rebalance_thread import RebalanceThread


def simplegesture(name, point_list):
    g = Gesture()
    g.add_stroke(point_list)
    g.normalize()
    g.name = name
    return g


class GesturesDelegate:
    def __init__(self, overlay):
        """
        Delegate's constructor. Simply binds to the data_manager.
        """
        self.overlay = overlay
        data_manager.data_man.bind(channels_widget_ux_mode=self.reset)

    def init_gdb(self, channels_widget):
        """
        Init gestures database with the gestures for each channel.
        """
        self.channels_widget = channels_widget
        self.in_gdb, self.out_gdb = GestureDatabase(), GestureDatabase()
        self.in_channel, self.out_channel = None, None
        for i, chan_id in enumerate(channels_widget.channels.sorted_chan_ids):
            channels_widget.cn[chan_id].update_rect(i, len(channels_widget.cn))
            self.in_gdb.add_gesture(channels_widget.cn[chan_id].gesture_in)
            self.out_gdb.add_gesture(channels_widget.cn[chan_id].gesture_out)

    def reset(self, *_):
        """
        Reset the delegate's channels.
        """
        self.in_channel, self.out_channel = None, None
        self.overlay.canvas.clear()

    def on_touch_down(self, touch):
        """
        Delegated on_touch_down event for the ChannelsWidget.
        Apply the inverse transformation Matrix to the point
        so they are in the Scatter's local space.
        """
        x, y, _ = self.channels_widget.transform.inverse().transform_point(
            touch.x, touch.y, 0
        )
        with self.overlay.canvas:
            Color(0.5, 0.5, 1, 0.3)
            d = 10.0
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud["line"] = Line(points=(touch.x, touch.y), width=5)
            touch.ud["line_local"] = [x, y]

    def on_touch_up(self, touch):
        """
        Delegated on_touch_up event for the ChannelsWidget.
        Apply the inverse transformation Matrix to the point
        so they are in the Scatter's local space.
        """
        if not touch.ud.get("line"):
            return

        with self.overlay.canvas:
            d = 10.0
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))

        if not self.out_channel:
            self.out_channel = self.get_match(self.in_gdb, touch)
            if self.out_channel:
                print(f"Selected out channel is: {self.out_channel}")
                self.channels_widget.cn[self.out_channel].l.flash(rgba=[0, 0, 1, 1])
        elif self.out_channel and not self.in_channel:
            self.in_channel = self.get_match(self.out_gdb, touch)
            if self.out_channel and self.in_channel:
                print(f"Selected in channel is: {self.in_channel}")
                self.channels_widget.cn[self.in_channel].l.flash(rgba=[0, 0, 1, 1])

        if self.out_channel and self.in_channel:
            channels = data_manager.data_man.channels
            last_hop_pubkey = next(
                c.remote_pubkey for c in channels if c.chan_id == self.in_channel
            )

            data_manager.data_man.channels_widget_ux_mode = 0

            thread = RebalanceThread(
                amount=1_000,
                chan_id=self.out_channel,
                last_hop_pubkey=last_hop_pubkey,
                fee_rate=500,
                max_paths=1000,
                name="RebalanceThread",
                thread_n=0,
            )
            thread.daemon = True
            thread.start()
            self.reset()

    def get_match(self, gdb, touch):
        """
        Find channel that matches the given gesture, in the given
        gesture database.
        """
        gesture_match = gdb.find(
            simplegesture(
                "",
                list(
                    zip(
                        touch.ud["line_local"][::2],
                        touch.ud["line_local"][1::2],
                    )
                ),
            ),
            minscore=0.70,
        )

        if gesture_match:
            return gesture_match[1].name

    def on_touch_move(self, touch):
        """
        Delegated on_touch_move event for the ChannelsWidget.
        Apply the inverse transformation Matrix to the point
        so they are in the Scatter's local space.
        """
        x, y, _ = self.channels_widget.transform.inverse().transform_point(
            touch.x, touch.y, 0
        )
        try:
            touch.ud["line"].points += [touch.x, touch.y]
            touch.ud["line_local"] += [x, y]
        except (KeyError) as e:
            pass
        return False
