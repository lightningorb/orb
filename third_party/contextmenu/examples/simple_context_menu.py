import kivy
from kivy.app import App
from kivy.lang import Builder

kivy.require('1.9.0')

import kivy_garden.contextmenu


kv = """
FloatLayout:
    id: layout
    Label:
        pos: 10, self.parent.height - self.height - 10
        text: "Left click anywhere outside the context menu to close it"
        size_hint: None, None
        size: self.texture_size

    Button:
        size_hint: None, None
        pos_hint: {"center_x": 0.5, "center_y": 0.8 }
        size: 300, 40
        text: "Click me to show the context menu"
        on_release: context_menu.show(*app.root_window.mouse_pos)

    ContextMenu:
        id: context_menu
        visible: False
        cancel_handler_widget: layout

        ContextMenuTextItem:
            text: "SubMenu #2"
        ContextMenuTextItem:
            text: "SubMenu #3"
            ContextMenu:
                ContextMenuTextItem:
                    text: "SubMenu #5"
                ContextMenuTextItem:
                    text: "SubMenu #6"
                    ContextMenu:
                        ContextMenuTextItem:
                            text: "SubMenu #9"
                        ContextMenuTextItem:
                            text: "SubMenu #10"
                        ContextMenuTextItem:
                            text: "SubMenu #11"
                        ContextMenuTextItem:
                            text: "Hello, World!"
                            on_release: app.say_hello(self.text)
                        ContextMenuTextItem:
                            text: "SubMenu #12"
                ContextMenuTextItem:
                    text: "SubMenu #7"
        ContextMenuTextItem:
            text: "SubMenu #4"
"""

class MyApp(App):

    def build(self):
        self.title = 'Simple context menu example'
        return Builder.load_string(kv)

    def say_hello(self, text):
        print(text)
        self.root.ids['context_menu'].hide()


if __name__ == '__main__':
    MyApp().run()