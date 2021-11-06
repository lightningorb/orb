from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField


class AEChannel(GridLayout):
    channel = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(AEChannel, self).__init__(*args, **kwargs)
        self.add_widget(Label(text="         "))
        for field in self.channel.ListFields():
            if field[0].type == 8:
                widget = BoxLayout(
                    orientation="horizontal", height=100, size_hint_y=None
                )
                widget.add_widget(Label(text=field[0].name))
                widget.add_widget(MDCheckbox(active=field[1]))
                self.add_widget(widget)
            elif field[0].type == 11:
                self.add_widget(Label(text="         "))
                self.add_widget(Label(text=field[0].name))
                try:
                    for f in field[1].DESCRIPTOR.fields:
                        widget = MDTextField(
                            helper_text=f.name,
                            helper_text_mode="persistent",
                            text=str(getattr(field[1], f.name)),
                        )
                        self.add_widget(widget)
                except:
                    pass
            else:
                widget = MDTextField(
                    helper_text=field[0].name,
                    helper_text_mode="persistent",
                    text=str(field[1]),
                )
                self.add_widget(widget)
        self.add_widget(Label(text="         "))