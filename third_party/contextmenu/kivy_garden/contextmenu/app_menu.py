from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder
import kivy.properties as kp
import os

from .context_menu import AbstractMenu, AbstractMenuItem, AbstractMenuItemHoverable, HIGHLIGHT_COLOR


class AppMenu(StackLayout, AbstractMenu):
    bounding_box = kp.ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(AppMenu, self).__init__(*args, **kwargs)
        self.hovered_menu_item = None

    def update_height(self):
        max_height = 0
        for widget in self.menu_item_widgets:
            if widget.height > max_height:
                max_height = widget.height
        return max_height

    def on_children(self, obj, new_children):
        for w in new_children:
            # bind events that update app menu height when any of its children resize
            w.bind(on_size=self.update_height)
            w.bind(on_height=self.update_height)

    def get_context_menu_root_parent(self):
        return self

    def self_or_submenu_collide_with_point(self, x, y):
        collide_widget = None

        # Iterate all siblings and all children
        for widget in self.menu_item_widgets:
            widget_pos = widget.to_window(0, 0)
            if widget.collide_point(x - widget_pos[0], y - widget_pos[1]) and not widget.disabled:
                if self.hovered_menu_item is None:
                    self.hovered_menu_item = widget

                if self.hovered_menu_item != widget:
                    self.hovered_menu_item = widget
                    for sibling in widget.siblings:
                        sibling.state = 'normal'

                    if widget.state == 'normal':
                        widget.state = 'down'
                        widget.on_release()

                    for sib in widget.siblings:
                        sib.hovered = False
            elif widget.get_submenu() is not None and not widget.get_submenu().visible:
                widget.state = 'normal'

        return collide_widget

    def close_all(self):
        for submenu in [w.get_submenu() for w in self.menu_item_widgets if w.get_submenu() is not None]:
            submenu.hide()
        for w in self.menu_item_widgets:
            w.state = 'normal'

    def hide_app_menus(self, obj, pos):
        if not self.collide_point(pos.x, pos.y):
            for w in [w for w in self.menu_item_widgets if not w.disabled and w.get_submenu().visible]:
                submenu = w.get_submenu()
                if submenu.self_or_submenu_collide_with_point(pos.x, pos.y) is None:
                    self.close_all()
                    self._cancel_hover_timer()


class AppMenuTextItem(ToggleButton, AbstractMenuItem):
    label = kp.ObjectProperty(None)
    text = kp.StringProperty('')
    font_size = kp.NumericProperty(14)
    color = kp.ListProperty([1, 1, 1, 1])
    hl_color = kp.ListProperty(HIGHLIGHT_COLOR)

    def on_release(self):
        submenu = self.get_submenu()

        if self.state == 'down':
            root = self._root_parent
            submenu.bounding_box_widget = root.bounding_box if root.bounding_box else root.parent

            submenu.bind(visible=self.on_visible)
            submenu.show(self.x, self.y - 1)

            for sibling in self.siblings:
                if sibling.get_submenu() is not None:
                    sibling.state = 'normal'
                    sibling.get_submenu().hide()

            self.parent._setup_hover_timer()
        else:
            self.parent._cancel_hover_timer()
            submenu.hide()

    def on_visible(self, *args):
        submenu = self.get_submenu()
        if self.width > submenu.get_max_width():
            submenu.width = self.width

    def _check_submenu(self):
        super(AppMenuTextItem, self)._check_submenu()
        self.disabled = (self.get_submenu() is None)

    # def on_mouse_down(self):
    #     print('on_mouse_down')
    #     return True


_path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(_path, 'app_menu.kv'))
