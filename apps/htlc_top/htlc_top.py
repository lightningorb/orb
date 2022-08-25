# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-07 13:12:23

import os
from pathlib import Path
from threading import Thread
from functools import lru_cache

import arrow
from peewee import Model, SqliteDatabase, CharField, BooleanField

from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivymd.uix.datatables import MDDataTable

from orb.misc.plugin import Plugin
from orb.store.model import Htlc
from orb.ln import Ln


class HtlcItem(Label):
    def __init__(self, in_id, out_id):
        super(HtlcItem, self).__init__()
        self.in_id = in_id
        self.out_id = out_id
        self.text = f"{in_id:<10}{out_id:<10}"


class HtlcTopView(Popup):
    def open(self, *args, **kwargs):
        """
        This gets called when the popup is first opened.
        """
        super(HtlcTopView, self).open(*args, **kwargs)
        app = App.get_running_app()
        ln = Ln()

        col_data = [
            ("Last Update", dp(60)),
            # ("in id", dp(20)),
            # ("out id", dp(20)),
            ("Type", dp(25)),
            ("Event Outcome", dp(50)),
            ("In Channel", dp(35)),
            ("In Alias", dp(50)),
            ("Out Channel", dp(35)),
            ("Out Alias", dp(50)),
            ("Amount", dp(30)),
            ("Fee", dp(30)),
            ("Detail", dp(150)),
        ]

        layout = GridLayout(
            cols=len(col_data), spacing=10, size_hint_y=None, size_hint_x=None
        )
        layout.bind(minimum_height=layout.setter("height"))
        layout.bind(minimum_width=layout.setter("width"))
        root = ScrollView(size_hint=(1, 1))
        root.add_widget(layout)
        self.add_widget(root)

        @mainthread
        def add_labels():
            for i, c in enumerate(col_data):
                label = Label(
                    text=c[0],
                    size_hint_y=None,
                    size_hint_x=None,
                    width=dp(c[1]) * 3,
                    height=40,
                    halign="left",
                    valign="middle",
                )

                label.bind(size=label.setter("text_size"))
                layout.add_widget(label)

        @mainthread
        def update(data, width):
            label = Label(
                text=data,
                size_hint_y=None,
                size_hint_x=None,
                width=dp(width * 3),
                height=40,
                halign="left",
                valign="middle",
            )
            label.bind(size=label.setter("text_size"))
            layout.add_widget(label)

        def func():
            add_labels()
            sizes = [x[1] for x in col_data]
            row_data = {}

            for e in Htlc.select().order_by(Htlc.timestamp.desc()).limit(100):
                if e.incoming_channel_id:
                    in_channel = app.channels.channels[e.incoming_channel_id]
                    in_alias = ln.get_node_alias(in_channel.remote_pubkey)
                else:
                    in_alias = ""
                if e.outgoing_channel_id:
                    out_channel = app.channels.channels[e.outgoing_channel_id]
                    out_alias = ln.get_node_alias(out_channel.remote_pubkey)
                else:
                    out_alias = ""
                if e.event_outcome_info:
                    amount = f'{int(e.event_outcome_info["incoming_amt_msat"]/1000):_}'
                else:
                    amount = "0"

                if e.link_fail_event:
                    detail = f"{e.link_fail_event['failure_detail']} {e.link_fail_event['failure_string'][:10]} {e.link_fail_event['wire_failure']}"
                else:
                    detail = ""

                row = (
                    arrow.get(e.timestamp).humanize(granularity=["minute", "second"]),
                    # e.incoming_htlc_id,
                    # e.outgoing_htlc_id,
                    e.event_type[:4],
                    e.event_outcome,
                    e.incoming_channel_id,
                    in_alias,
                    e.outgoing_channel_id,
                    out_alias,
                    amount,
                    0,
                    detail,
                )
                row_data[e.incoming_htlc_id] = row

            for row in row_data:
                for i, c in enumerate(row_data[row]):
                    update(str(c), sizes[i])

        def run(*_):
            layout.clear_widgets()
            t = Thread(target=func)
            t.start()

        Clock.schedule_once(run, 0)
        self.sc = Clock.schedule_interval(run, 60)

    def dismiss(self):
        super(HtlcTopView, self).dismiss()
        Clock.unschedule(self.sc)


class HtlcTopPlugin(Plugin):
    def main(self):
        """
        Main function. The caller must call this.
        """
        kv_path = (Path(__file__).parent / "htlc_top.kv").as_posix()
        Builder.unload_file(kv_path)
        Builder.load_file(kv_path)
        HtlcTopView().open()
