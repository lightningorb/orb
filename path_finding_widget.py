import math
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout

from data_manager import data_man, controllers
from channel_widget import ChannelWidget


class PathFindingLayout(RelativeLayout):
    pass


class PathFindingWidget(Scatter):
    def __init__(self, **kwargs):
        super(PathFindingWidget, self).__init__(**kwargs)
        controllers["path_finding_widget"] = self

    def build(self):
        pass

    def update_rect(self, *args):
        pass
