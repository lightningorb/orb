from kivy.animation import Animation
from kivy.properties import ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.button import Button
import data_manager
from threading import Thread
from orb.misc.utils import prefs_col, pref


class Node(Button):
    attribute_editor = ObjectProperty(None)
    col = ListProperty([0, 0, 0, 0])
    channel = ObjectProperty(None)
    touch_start = ListProperty([0, 0])
    touch_end = ListProperty([0, 0])
    round = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self.col = prefs_col('display.node_background_color')
        lnd = data_manager.data_man.lnd
        if self.channel:
            Thread(
                target=lambda: setattr(
                    self, "text", lnd.get_node_alias(self.channel.remote_pubkey)
                )
            ).start()

    def anim_to_pos(self, pos):
        Animation(pos=pos, duration=1).start(self)

    def on_release(self):
        self.col = prefs_col('display.node_selected_background_color')
        ae = self.attribute_editor
        ae.selection = self.text
        if self.channel:
            ae.channel = self.channel

    def on_press(self):
        self.col = prefs_col('display.node_selected_background_color')

    def on_touch_down(self, touch):
        import data_manager

        if self.collide_point(*touch.pos):
            if data_manager.data_man.menu_visible:
                return False
        return super(Node, self).on_touch_down(touch)

    @property
    def width_pref(self):
        return pref('display.node_height') if self.round else pref('display.node_width')

    @property
    def height_pref(self):
        return pref('display.node_height')
