# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-05 05:00:12

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField

from orb.misc.prefs import is_rest
from orb.misc.auto_obj import AutoObj

import data_manager


class MyMDCheckbox(MDCheckbox):
    """
    Custom MDCheckbox implementation. The hopes is to disable clicking
    which is a lot harder than it sounds.

    :param MDCheckbox: The checkbox object.
    :type MDCheckbox: MDCheckbox
    """

    def on_touch_down(self, *args):
        """
        Invoked whenever the checkbox is clicked by the user.

        :return: Whether to propagate events.
        :rtype: bool
        """
        return False


class AEChannel(GridLayout):
    """
    The Attributes Editor can display anything (not just channels).
    This is the class for displaying channels.

    :param GridLayout: [description]
    :type GridLayout: [type]
    """

    #: The channel being represented by this instance.
    channel = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        """
        Class constructor.
        """

        super(AEChannel, self).__init__(*args, **kwargs)
        self.add_widget(Label(text="         "))

        if is_rest():
            self.populate_rest()
        else:
            self.populate_grpc()

    def populate_rest(self):
        """
        Populate fields when using the REST API.
        """
        c = self.channel.__dict__
        for field in c:
            if type(c[field]) is bool:
                widget = BoxLayout(
                    orientation="horizontal", height=100, size_hint_y=None
                )
                widget.add_widget(Label(text=field))
                widget.add_widget(MDCheckbox(active=c[field]))
                widget.readonly = True
                self.add_widget(widget)
            elif type(c[field]) is AutoObj:
                self.add_widget(Label(text="         "))
                self.add_widget(Label(text=field))
                try:
                    for f in c[field]:
                        widget = MDTextField(
                            helper_text=f,
                            helper_text_mode="persistent",
                            text=str(c[field][f]),
                        )
                        self.add_widget(widget)
                        widget.cursor = (0, 0)
                        widget.readonly = True
                except:
                    pass
            elif type(c[field]) in [int, str]:
                val = c[field]
                if type(c[field]) is int:
                    val = str(int(c[field]))
                widget = MDTextField(
                    helper_text=field, helper_text_mode="persistent", text=val
                )
                self.add_widget(widget)
                widget.readonly = True
        self.add_widget(Label(text="         "))

    def populate_grpc(self):
        """
        Populate fields when using the GRPC API.
        """
        for field in self.channel.ListFields():
            if field[0].type == 8:
                widget = BoxLayout(
                    orientation="horizontal", height=100, size_hint_y=None
                )
                widget.add_widget(Label(text=field[0].name))
                widget.add_widget(MDCheckbox(active=field[1]))
                self.add_widget(widget)
            elif field[0].type == 11:
                self.add_widget(Label(text="         "))
                self.add_widget(Label(text=field[0].name))
                try:
                    for f in field[1].DESCRIPTOR.fields:
                        widget = MDTextField(
                            helper_text=f.name,
                            helper_text_mode="persistent",
                            text=str(getattr(field[1], f.name)),
                        )
                        self.add_widget(widget)
                        widget.readonly = True
                except:
                    pass
            else:
                widget = MDTextField(
                    helper_text=field[0].name,
                    helper_text_mode="persistent",
                    text=str(field[1]),
                )
                widget.readonly = True
                self.add_widget(widget)
        self.add_widget(Label(text="         "))

    def pay_through_channel(self, active: bool):
        """
        Callback for when the 'pay through channel' checkbox is ticked.

        :param active: whether to activate or deactivate paying through channel.
        :type active: bool
        """
        vals = data_manager.data_man.store.get("pay_through_channel", {})
        vals[str(self.channel.chan_id)] = active
        data_manager.data_man.store.put("pay_through_channel", **vals)

    def on_balanced_ratio(self, ratio: bool):
        """
        Callback for when the balance ratio field is modified.

        :param ratio: the desired ratio, between 0 and 1
        :type ratio: bool
        """
        vals = data_manager.data_man.store.get("balanced_ratio", {})
        vals[str(self.channel.chan_id)] = ratio
        data_manager.data_man.store.put("balanced_ratio", **vals)
