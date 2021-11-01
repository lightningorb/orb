from kivy.uix.effectwidget import EffectWidget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
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
    touch_start = ListProperty([0, 0])
    touch_end = ListProperty([0, 0])

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self.col = prefs_col('display.node_background_color')
        lnd = data_manager.data_man.lnd
        # with self.canvas:
        #     Color(*[1,0,0,1])
        #     self.rebalance_line = Line(points=[0, 0, 500, 500], width=2)
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

    def on_press(self):
        self.col = prefs_col('display.node_selected_background_color')

    def on_touch_down(self, touch):
        import data_manager

        if self.collide_point(*touch.pos):
            if data_manager.menu_visible:
                return False
        return super(Node, self).on_touch_down(touch)

    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         self.touch_start = touch.pos
    #         self.touch_end = touch.pos
    #         # self.rebalance_line.points[:2] = touch.pos
    #         # self.rebalance_line.points[2:] = touch.pos
    #         return True
    #     return super(Node, self).on_touch_down(touch)

    # def on_touch_move(self, touch):
    #     # self.rebalance_line.points[2:] = touch.pos
    #     if self.collide_point(*touch.pos):
    #         self.touch_end = touch.pos
    #         return True
    #     return super(Node, self).on_touch_move(touch)

    # def on_touch_up(self, touch):
    #     if self.collide_point(*touch.pos):
    #         self.on_release()
    #         self.touch_end = touch.pos
    #         return True
    #     return super(Node, self).on_touch_up(touch)
