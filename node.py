from kivy.animation import Animation
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.button import Button
import data_manager
from threading import Thread
from utils import prefs_col

class Node(Button):
    attribute_editor = ObjectProperty(None)
    col = ListProperty([0, 0, 0, 0])
    channel = ObjectProperty(None)

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
