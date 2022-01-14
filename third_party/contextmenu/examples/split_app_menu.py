import kivy
from random import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.logger import Logger
import logging

kivy.require('1.9.0')
# Logger.setLevel(logging.DEBUG)

import kivy_garden.contextmenu

kv = """
RelativeLayout:
    canvas.before:
        Color:
            rgb: app.random_color()
        Rectangle:
            pos: 0, 0
            size: self.size
    AppMenu:
        id: menu
        top: self.parent.height
        AppMenuTextItem:
            text: "Menu"
            ContextMenu:
                ContextMenuTextItem:
                    text: "Item #1"
                ContextMenuTextItem:
                    text: "Item #2"
"""

class MyApp(App):

    def build(self):
        self.title = 'Simple app menu example'

        layout = GridLayout(cols=2, rows=2)
        for i in range(0, 4):
            widget = Builder.load_string(kv)
            widget.ids['menu'].cancel_handler_widget = layout
            layout.add_widget(widget)

        return layout

    def random_color(self):
        return random(), random(), random()

if __name__ == '__main__':
    MyApp().run()