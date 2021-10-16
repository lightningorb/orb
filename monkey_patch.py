def patch_settings():

    from kivy.uix.settings import SettingItem
    from kivy.uix.label import Label

    def add_widget(self, *largs):
        largs = [*largs]
        if largs and type(largs[0]) is Label:
            value = self.panel.get_value(self.section, self.key)[:20]
            largs[0] = Label(text=value)
        if self.content is None:
            return super(SettingItem, self).add_widget(*largs)
        return self.content.add_widget(*largs)

    SettingItem.add_widget = add_widget
