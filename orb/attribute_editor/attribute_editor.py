# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-27 16:41:23

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from orb.attribute_editor.AE_channel import AEChannel


class AttributeEditor(BoxLayout):
    """
    The AttributeEditor opens on the right side of the screen
    when a peer is selected in the application.
    """

    #: The currently selected peer.
    selection = ObjectProperty("")

    #: The currently selected channel object.
    channel = ObjectProperty(None, allownone=True)

    def __init__(self, *args, **kwargs):
        """
        Class constructor.
        """
        super(AttributeEditor, self).__init__(*args, **kwargs)
        self.bind(channel=self.on_selection_changed)

    def on_selection_changed(self, *_):
        """
        Invoked whenever a peer is selected.
        """
        self.ids.ae_scroll_view.clear_widgets()
        if self.selection:
            self.ids.ae_scroll_view.add_widget(
                AEChannel(
                    channel=self.channel,
                    pos=[self.pos[0], self.pos[1] + 50],
                    size=[self.size[0], self.size[1] - 100],
                )
            )

    def clear(self):
        """
        Clear the selection.
        """
        self.ids.ae_scroll_view.clear_widgets()
        self.selection = ""
        self.channel = None

    def on_touch_down(self, touch):
        """
        Detect when the user touched inside the AttributeEditor.
        """
        if self.collide_point(*touch.pos):
            if touch.is_mouse_scrolling:
                self.ids.ae_scroll_view.on_touch_down(touch)
                return True
        return super(AttributeEditor, self).on_touch_down(touch)
