Kivy Context Menu
=================

Collection of classes for easy creating **context** and **application** menus.

Please see the garden [instructions](https://kivy-garden.github.io) for how to use kivy garden flowers.

Flower information
-------------------

## Context Menu

![Example of context menu](https://raw.githubusercontent.com/kivy-garden/garden.contextmenu/master/doc/context-menu-01.png)

Context menu is represented by `ContextMenu` widget that wraps all menu items as `ContextMenuTextItem` widgets. Context menus can be nested, each `ContextMenuTextItem` can contain maximum one `ContextMenu` widget.

```python
import kivy
from kivy.app import App
from kivy.lang import Builder
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
```

Arrows that symbolize that an item has sub menu is created automatically. `ContextMenuTextItem` inherits from [ButtonBehavior](http://kivy.org/docs/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) so you can use `on_release` to bind actions to it.

The root context menu can use `cancel_handler_widget` parameter. This adds `on_touch_down` event to it that closes the menu when you click anywhere outside the menu.


## Application Menu

![Example of application menu](https://raw.githubusercontent.com/kivy-garden/garden.contextmenu/master/doc/app-menu-01.png)

Creating application menus is very similar to context menus. Use `AppMenu` and `AppMenuTextItem` widgets to create the top level menu. Then each `AppMenuTextItem` can contain one `ContextMenu` widget as we saw above. `AppMenuTextItem` without `ContextMenu` are disabled by default

```python
import kivy
from kivy.app import App
from kivy.lang import Builder
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
                        # ...
                ContextMenuTextItem:
                    text: "Item #5"
        AppMenuTextItem:
            text: "Menu Menu #3"
            ContextMenu:
                ContextMenuTextItem:
                    text: "SubMenu #31"
                ContextMenuDivider:
                ContextMenuTextItem:
                    text: "SubMenu #32"
                # ...
        AppMenuTextItem:
            text: "Menu #4"
    # ...
    # The rest follows as usually
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
```

Install
-------

```sh
pip install kivy_garden.contextmenu
```

Usage
-----

### All classes

`garden.contextmenu` provides you with a set of classes and mixins for creating your own customised menu items for both context and application menus.

#### context_menu.AbstractMenu

Mixin class that represents basic functionality for all menus. It cannot be used by itself and needs to be extended with a layout. Provides `cancel_handler_widget` property. See [AppMenu](https://github.com/kivy-garden/garden.contextmenu/blob/master/app_menu.py) or [ContextMenu](https://github.com/kivy-garden/garden.contextmenu/blob/master/context_menu.py).

#### context_menu.ContextMenu

Implementation of a context menu.

#### context_menu.AbstractMenuItem

Mixin class that represents a single menu item. Needs to be extended to be any useful. It's a base class for all menu items for both context and application menus.

If you want to extend this class you need to override the `content_width` property which tells the parent `ContextMenu` what is the expected width of this item. It needs to know this to set it's own width.

#### context_menu.ContextMenuItem

Single context menu item. Automatically draws an arrow if contains a `ContextMenu` children. If you want to create a custom menu item extend this class.

#### context_menu.AbstractMenuItemHoverable

Mixin class that makes any class that inherits `ContextMenuItem` to change background color on mouse hover.

#### context_menu.ContextMenuText

Menu item with `Label` widget without any extra functionality.

#### context_menu.ContextMenuDivider

Menu widget that splits two parts of a context/app menu.

![Example of ContextMenuDivider without text](https://raw.githubusercontent.com/kivy-garden/garden.contextmenu/master/doc/menu-divider-01.png)

It also contains an instance of `Label` which is not visible if you don't set it any text.

```python
ContextMenuTextItem:
    text: "SubMenu #33"
ContextMenuDivider:
    text: "More options"
ContextMenuTextItem:
    text: "SubMenu #34"
```

![Example of ContextMenuDivider with text](https://raw.githubusercontent.com/kivy-garden/garden.contextmenu/master/doc/menu-divider-02.png)

#### context_menu.ContextMenuTextItem

Menu item with text. You'll be most of the time just fine using this class for all your menu items. You can also see it used in [all examples here](https://github.com/kivy-garden/garden.contextmenu/tree/master/examples).  Contains a `Label` widget and copies `text`, `font_size` and `color` properties to it automatically.

#### app_menu.AppMenu

Application menu widget. By default it fills the entire parent's width.

#### app_menu.AppMenuTextItem

Application menu item width text. Contains a `Label` widget and copies `text`, `font_size` and `color` properties to it automatically.

Contributing
--------------

Check out our [contribution guide](CONTRIBUTING.md) and feel free to improve the flower.

License
---------

This software is released under the terms of the MIT License.
Please see the [LICENSE.txt](LICENSE.txt) file.
