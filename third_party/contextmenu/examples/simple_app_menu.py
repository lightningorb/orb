import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
import logging

kivy.require('1.9.0')
# Logger.setLevel(logging.DEBUG)

import kivy_garden.contextmenu

kv = """
FloatLayout:
    id: layout
    AppMenu:
        id: app_menu
        top: root.height
        cancel_handler_widget: layout

        AppMenuTextItem:
            text: "Menu #1"
            ContextMenu:
                ContextMenuTextItem:
                    text: "Item #11"
                ContextMenuTextItem:
                    text: "Item #12"
        AppMenuTextItem:
            text: "Menu Menu Menu #2"
            ContextMenu:
                ContextMenuTextItem:
                    text: "Item #21"
                ContextMenuTextItem:
                    text: "Item #22"
                ContextMenuTextItem:
                    text: "ItemItemItem #23"
                ContextMenuTextItem:
                    text: "Item #24"
                    ContextMenu:
                        ContextMenuTextItem:
                            text: "Item #241"
                        ContextMenuTextItem:
                            text: "Hello, World!"
                            on_release: app.say_hello(self.text)
                        ContextMenuTextItem:
                            text: "Item #243"
                        ContextMenuTextItem:
                            text: "Item #244"
                ContextMenuTextItem:
                    text: "Item #5"
        AppMenuTextItem:
            text: "Menu Menu #3"
            ContextMenu:
                ContextMenuTextItem:
                    text: "SubMenu #31"
                ContextMenuTextItem:
                    text: "SubMenu #32"
                ContextMenuTextItem:
                    text: "SubMenu #33"
                ContextMenuDivider:
                ContextMenuTextItem:
                    text: "SubMenu #34"
        AppMenuTextItem:
            text: "Menu #4"

    Label:
        pos: 10, 10
        text: "Left click anywhere outside the context menu to close it"
        size_hint: None, None
        size: self.texture_size
"""


class MyApp(App):

    def build(self):
        self.title = 'Simple app menu example'
        return Builder.load_string(kv)

    def say_hello(self, text):
        print(text)
        self.root.ids['app_menu'].close_all()

if __name__ == '__main__':
    MyApp().run()
