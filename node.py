from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.button import Button


class Node(Button):
    attribute_editor = ObjectProperty(None)
    col = ListProperty([80 / 255, 80 / 255, 80 / 255, 1])
    channel = ObjectProperty(None)

    def on_release(self):
        print("on release")
        self.col = [150 / 255, 150 / 255, 150 / 255, 1]
        ae = self.attribute_editor
        ae.selection_type = "node"
        ae.selection = self.text
        if self.channel:
            ae.channel = self.channel
