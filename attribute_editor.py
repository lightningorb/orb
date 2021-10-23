from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from AE_channel import AEChannel
from AE_fees import AEFees


class AttributeEditor(BoxLayout):
    selection = ObjectProperty("")
    channel = ObjectProperty(None, allownone=True)

    def __init__(self, *args, **kwargs):
        super(AttributeEditor, self).__init__(*args, **kwargs)
        self.bind(channel=self.on_selection_changed)

    def on_selection_changed(self, *_):
        self.ids.ae_scroll_view.clear_widgets()
        if self.selection:
            self.ids.ae_scroll_view.add_widget(
                AEChannel(
                    channel=self.channel,
                    pos=[self.pos[0], self.pos[1] + 50],
                    size=[self.size[0], self.size[1] - 100],
                )
            )

    def clear(self):
        self.ids.ae_scroll_view.clear_widgets()
        self.selection = ""
        self.channel = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_mouse_scrolling:
                self.ids.ae_scroll_view.on_touch_down(touch)
                return True
        return super(AttributeEditor, self).on_touch_down(touch)
