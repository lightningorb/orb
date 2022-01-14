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
FloatLayout:
    canvas.before:
        Color:
            rgb: app.random_color()
        Rectangle:
            pos: self.pos
            size: self.size

    Button:
        size_hint: None, None
        pos_hint: {"center_x": 0.5, "center_y": 0.8 }
        size: 300, 40
        text: "Click me to show the context menu"
        on_release: app.show_context_menu(context_menu)

    ContextMenu:
        id: context_menu
        # visible: False
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
            widget.ids['context_menu'].cancel_handler_widget = layout
            layout.add_widget(widget)

        return layout

    def random_color(self):
        return random(), random(), random()

    def show_context_menu(self, context_menu):
        print(self.root_window.mouse_pos)
        context_menu.show(*self.root_window.mouse_pos)

if __name__ == '__main__':
    MyApp().run()