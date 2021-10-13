import threading
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.button import Button
import data_manager
from threading import Thread

class Node(Button):
    attribute_editor = ObjectProperty(None)
    col = ListProperty([80 / 255, 80 / 255, 80 / 255, 1])
    channel = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        lnd = data_manager.data_man.lnd
        if self.channel:
            Thread(target=lambda: setattr(self, 'text', lnd.get_node_alias(self.channel.remote_pubkey))).start()

    def on_release(self):
        self.col = [150 / 255, 150 / 255, 150 / 255, 1]
        ae = self.attribute_editor
        ae.selection_type = "node"
        ae.selection = self.text
        if self.channel:
            ae.channel = self.channel
