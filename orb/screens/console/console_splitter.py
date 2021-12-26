from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.splitter import Splitter


class ConsoleSplitter(Splitter):

    input = ObjectProperty(None)
    output = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(ConsoleSplitter, self).__init__(*args, **kwargs)
        self.pressed = False
        self.pressed_pos = (0, 0)
        self.input_pressed_height = 0
        self.output_pressed_height = 0

        def load_config(*_):
            import data_manager

            input_height = data_manager.data_man.store.get("console", {}).get(
                "input_height", None
            )
            output_height = data_manager.data_man.store.get("console", {}).get(
                "output_height", None
            )

            if input_height and output_height:
                self.input.height = input_height
                self.output.height = output_height
                self.input.size_hint = (1, None)
                self.output.size_hint = (1, None)

        Clock.schedule_once(load_config, 1)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = True
            self.pressed_pos = touch.pos
            self.input_pressed_height = self.input.height
            self.output_pressed_height = self.output.height
        return super(ConsoleSplitter, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = False
        return super(ConsoleSplitter, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        import data_manager

        if self.pressed:
            self.input.height = self.input_pressed_height + (
                self.pressed_pos[1] - touch.pos[1]
            )
            self.output.height = self.output_pressed_height - (
                self.pressed_pos[1] - touch.pos[1]
            )
            data_manager.data_man.store.put(
                "console",
                input_height=self.input.height,
                output_height=self.output.height,
            )
            self.input.size_hint = (1, None)
            self.output.size_hint = (1, None)
            return True
        return super(ConsoleSplitter, self).on_touch_move(touch)