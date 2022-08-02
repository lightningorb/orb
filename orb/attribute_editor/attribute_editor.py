# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 10:41:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-01 10:51:09

from threading import Thread

from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivymd.uix.list import MDList, OneLineIconListItem
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.clock import mainthread
from kivy.app import App

from orb.misc.decorators import guarded
from orb.misc.prefs import is_rest
from orb.misc.auto_obj import AutoObj, todict
from orb.lnd import Lnd

from orb.misc import data_manager


class MyMDCheckbox(MDCheckbox):
    """
    Custom MDCheckbox implementation. The hopes is to disable clicking
    which is a lot harder than it sounds.

    :param MDCheckbox: The checkbox object.
    :type MDCheckbox: MDCheckbox
    """

    def on_touch_down(self, event):
        """
        Invoked whenever the checkbox is clicked by the user.

        :return: Whether to propagate events.
        :rtype: bool
        """
        if self.collide_point(event.pos[0], event.pos[1]):
            return False
        return super(MyMDCheckbox, self).on_touch_down(event)


class DrawerList(MDList):
    pass


class AttributeEditor(BoxLayout):

    alias = StringProperty("")
    identity_pubkey = StringProperty("")

    #: The currently selected channel object.
    channel = ObjectProperty(None, allownone=True)

    def __init__(self, *args, **kwargs):
        """
        Class constructor.
        """
        super(AttributeEditor, self).__init__(*args, **kwargs)

        def update_channel(inst, channel):
            self.channel = channel

        App.get_running_app().bind(selection=update_channel)

    def clear(self):
        """
        Clear the selection.
        """
        self.ids.md_list.clear_widgets()
        self.channel = None
        self.alias = ""
        self.identity_pubkey = ""

    def on_channel(self, inst, channel):
        """
        Invoked whenever a channel is selected.
        """
        if channel:

            @mainthread
            def update(*_):
                self.size_hint_y = None
                if self.channel:
                    self.alias = self.channel.alias
                    self.identity_pubkey = self.channel.remote_pubkey
                    self.ids.md_list.clear_widgets()
                    self.populate_earned()
                    self.populate_helped_earn()
                    # self.populate_debt()
                    self.populate_profit()
                    self.populate_fees()
                    if is_rest():
                        self.populate_rest(c=self.channel.channel.__dict__)
                    else:
                        self.populate_grpc()

            Clock.schedule_once(update, 0.25)
        else:
            self.clear()

    @guarded
    def populate_earned(self):
        @mainthread
        def update(val):
            self.ids.earned.text = val

        self.ids.earned.text = ""
        Thread(
            target=lambda: update(
                "{:_}".format(self.channel.earned if self.channel else 0)
            )
        ).start()

    @guarded
    def populate_helped_earn(self):
        @mainthread
        def update(val):
            self.ids.helped_earn.text = val

        self.ids.helped_earn.text = ""
        Thread(
            target=lambda: update(
                "{:_}".format(self.channel.helped_earn if self.channel else 0)
            )
        ).start()

    @guarded
    def populate_profit(self):
        @mainthread
        def update(val):
            self.ids.profit.text = val

        self.ids.profit.text = ""
        Thread(
            target=lambda: update(
                "{:_}".format(self.channel.profit if self.channel else 0)
            )
        ).start()

    # @guarded
    # def populate_debt(self):
    #     @mainthread
    #     def update(val):
    #         self.ids.debt.text = val

    #     self.ids.debt.text = ""
    #     Thread(
    #         target=lambda: update(
    #             "{:_}".format(self.channel.debt if self.channel else 0)
    #         )
    #     ).start()

    @guarded
    def fee_rate_milli_msat_changed(self, val, *args):
        """
        Invoked whenever the fee rate is changed.
        """
        val = int(val.text)
        if val != self.channel.fee_rate_milli_msat:
            self.channel.fee_rate_milli_msat = val

    @guarded
    def fee_base_msat_changed(self, val):
        """
        Invoked whenever the fee base rate is changed.
        """
        val = int(val.text)
        if val != self.channel.fee_base_msat:
            self.channel.fee_base_msat = val

    @guarded
    def min_htlc_changed(self, val):
        """
        Invoked whenever the min HTLC is changed.
        """
        val = int(val.text)
        if val != self.channel.min_htlc_msat:
            self.channel.min_htlc_msat = val

    @guarded
    def max_htlc_msat_changed(self, val):
        """
        Invoked whenever the max HTLC is changed.
        """
        val = int(val.text)
        if val != self.channel.max_htlc_msat:
            self.channel.max_htlc_msat = val

    @guarded
    def time_lock_delta_changed(self, val):
        """
        Invoked whenever timelock delta is changed.
        """
        val = int(val.text)
        if val != self.channel.time_lock_delta:
            self.channel.time_lock_delta = val

    def populate_rest(self, c):
        """
        Populate fields when using the REST API.
        """
        for field in c:
            if type(c[field]) is bool:
                widget = BoxLayout(orientation="horizontal", size_hint_y=None)
                widget.add_widget(Label(text=field))
                widget.add_widget(MyMDCheckbox(active=c[field]))
                widget.readonly = True
                self.ids.md_list.add_widget(widget)
                widget.height = dp(50)
            elif type(c[field]) is AutoObj:
                self.ids.md_list.add_widget(
                    MDLabel(text=field, size_hint_y=None, height=dp(50))
                )
                self.populate_rest(c=todict(c[field]))
            elif type(c[field]) in [int, str]:
                val = (
                    getattr(self.channel, field)
                    if hasattr(self.channel, field)
                    else c[field]
                )
                if type(val) is int:
                    val = f"{val:_}"
                widget = MDTextField(
                    helper_text=field,
                    helper_text_mode="persistent",
                    text=val,
                    height=dp(50),
                )
                self.ids.md_list.add_widget(widget)
                widget.readonly = True

    def populate_grpc(self):
        """
        Populate fields when using the GRPC API.
        """
        for field in self.channel.ListFields():
            if field[0].type == 8:
                widget = BoxLayout(orientation="horizontal", size_hint_y=None)
                widget.add_widget(MDLabel(text=field[0].name))
                widget.add_widget(MDCheckbox(active=field[1]))
                self.ids.md_list.add_widget(widget)
                widget.height = dp(50)
            elif field[0].type == 11:
                self.ids.md_list.add_widget(
                    Label(text=field[0].name, size_hint_y=None, height=dp(15))
                )
                try:
                    for f in field[1].DESCRIPTOR.fields:
                        if f.type in [3, 4] and f.name != "chan_id":
                            val = f"{getattr(field[1], f.name):_}"
                        else:
                            val = str(getattr(field[1], f.name))
                        widget = MDTextField(
                            helper_text=f.name,
                            helper_text_mode="persistent",
                            text=val,
                        )
                        self.ids.md_list.add_widget(widget)
                        widget.readonly = True
                except:
                    pass
            else:
                if field[0].type in [3, 4] and field[0].name != "chan_id":
                    val = f"{field[1]:_}"
                else:
                    val = str(field[1])
                widget = MDTextField(
                    helper_text=field[0].name,
                    helper_text_mode="persistent",
                    text=val,
                )
                widget.readonly = True
                self.ids.md_list.add_widget(widget)

    def pay_through_channel(self, active, widget):
        """
        Callback for when the 'pay through channel' checkbox is ticked.

        :param active: whether to activate or deactivate paying through channel.
        :type active: field
        """
        vals = App.get_running_app().store.get("pay_through_channel", {})
        vals[str(self.channel.chan_id)] = active.active
        App.get_running_app().store.put("pay_through_channel", **vals)

    def exclude_from_balanced_ratio(self, active, widget):
        """
        Callback for when the 'exclude from balanced ratio' checkbox is ticked.

        :param active: whether to activate or deactivate exclude from balanced ratio.
        :type active: field
        """
        vals = App.get_running_app().store.get("exclude_from_balanced_ratio", {})
        vals[str(self.channel.chan_id)] = active.active
        App.get_running_app().store.put("exclude_from_balanced_ratio", **vals)

    def on_balanced_ratio(self, ratio):
        """
        Callback for when the balance ratio field is modified.

        :param ratio: the desired ratio, between 0 and 1
        :type ratio: field
        """
        vals = App.get_running_app().store.get("balanced_ratio", {})
        if ratio.text == "":
            if str(self.channel.chan_id) in vals:
                del vals[str(self.channel.chan_id)]
        else:
            vals[str(self.channel.chan_id)] = float(ratio.text)
        App.get_running_app().store.put("balanced_ratio", **vals)

    def populate_fees(self):
        self.ids.md_list.add_widget(
            ItemDrawer(
                icon="boom-gate",
                text="Fees:",
            )
        )
        self.ids.md_list.add_widget(
            MDTextField(
                text=f"{self.channel.fee_rate_milli_msat:_}",
                helper_text="Fee Rate Milli Msat",
                helper_text_mode="persistent",
                on_text_validate=self.fee_rate_milli_msat_changed,
            )
        )
        self.ids.md_list.add_widget(
            MDTextField(
                text=f"{self.channel.fee_base_msat:_}",
                helper_text="Fee Base Msat",
                helper_text_mode="persistent",
                on_text_validate=self.fee_base_msat_changed,
            )
        )
        self.ids.md_list.add_widget(
            MDTextField(
                text=f"{self.channel.min_htlc_msat:_}",
                helper_text="Min HTLC msat",
                helper_text_mode="persistent",
                on_text_validate=self.min_htlc_changed,
            )
        )
        self.ids.md_list.add_widget(
            MDTextField(
                text=f"{self.channel.max_htlc_msat:_}",
                helper_text="Max HTLC msat",
                helper_text_mode="persistent",
                on_text_validate=self.max_htlc_msat_changed,
            )
        )
        self.ids.md_list.add_widget(
            MDTextField(
                text=f"{self.channel.time_lock_delta:_}",
                helper_text="Time Lock Delta",
                helper_text_mode="persistent",
                on_text_validate=self.time_lock_delta_changed,
            )
        )
        self.ids.md_list.add_widget(
            ItemDrawer(
                icon="arrow-expand-right",
                text="Pay through channel:",
                size_hint_y=None,
                height=dp(60),
            )
        )

        ptc = MDSwitch(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            active=App.get_running_app()
            .store.get("pay_through_channel", {})
            .get(str(self.channel.chan_id if self.channel else ""), True),
            size_hint_y=None,
            height=dp(50),
        )

        ptc.bind(active=self.pay_through_channel)

        self.ids.md_list.add_widget(ptc)

        self.ids.md_list.add_widget(
            ItemDrawer(
                icon="arrow-expand-right",
                text="Exclude from balanced ratio:",
                size_hint_y=None,
                height=dp(60),
            )
        )

        efbr = MDSwitch(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            active=App.get_running_app()
            .store.get("exclude_from_balanced_ratio", {})
            .get(str(self.channel.chan_id if self.channel else ""), False),
            size_hint_y=None,
            height=dp(50),
        )

        efbr.bind(active=self.exclude_from_balanced_ratio)

        self.ids.md_list.add_widget(efbr)

        self.ids.md_list.add_widget(
            ItemDrawer(
                icon="chart-bell-curve-cumulative",
                text="Balanced Ratio:",
                size_hint_y=None,
                height=dp(60),
            )
        )
        if self.channel:
            text = str(
                App.get_running_app()
                .store.get("balanced_ratio", {})
                .get(
                    str(self.channel.chan_id),
                    str(self.channel.balanced_ratio),
                )
            )
        else:
            text = "-1"
        self.ids.md_list.add_widget(
            MDTextField(
                text=text,
                helper_text="balanced ratio",
                helper_text_mode="persistent",
                on_text_validate=self.on_balanced_ratio,
            )
        )
        self.ids.md_list.add_widget(
            ItemDrawer(
                icon="abacus", text="Attributes:", size_hint_y=None, height=dp(60)
            )
        )


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
