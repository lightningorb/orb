import threading
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.button import Button
import data_manager


class Node(Button):
    attribute_editor = ObjectProperty(None)
    col = ListProperty([80 / 255, 80 / 255, 80 / 255, 1])
    channel = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        lnd = data_manager.data_man.lnd
        def thread_function():
            if self.channel:
                alias = lnd.get_node_alias(self.channel.remote_pubkey)
                self.text = alias
        x = threading.Thread(target=thread_function)
        x.start()

    def on_release(self):
        self.col = [150 / 255, 150 / 255, 150 / 255, 1]
        ae = self.attribute_editor
        ae.selection_type = "node"
        ae.selection = self.text
        if self.channel:
            ae.channel = self.channel
