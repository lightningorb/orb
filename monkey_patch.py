def patch_settings():

    from kivy.uix.settings import SettingItem
    from kivy.uix.label import Label

    def add_widget(self, *largs):
        largs = [*largs]
        if largs and type(largs[0]) is Label:
            print(self.section, self.key)
            if self.key in ['tls_certificate', 'macaroon_admin']:
                value = self.panel.get_value(self.section, self.key)[:20]
                largs[0] = Label(text=value)
        if self.content is None:
            return super(SettingItem, self).add_widget(*largs)
        return self.content.add_widget(*largs)

    SettingItem.add_widget = add_widget


def patch_store():
    from kivy.storage.jsonstore import JsonStore

    def get(self, key, default=None):
        try:
            return self.orig_get(key)
        except:
            return default

    JsonStore.orig_get = JsonStore.get
    JsonStore.get = get

def patch_kv_settings():
    from kivy.uix.settings import Settings

    def add_kivy_panel(self):
        from kivy import kivy_data_dir
        from kivy.config import Config
        from os.path import join
        self.add_json_panel('App Settings', Config, join(kivy_data_dir, 'settings_kivy.json'))

    Settings.add_kivy_panel = add_kivy_panel

def do_monkey_patching():
    patch_store()
    patch_settings()
    patch_kv_settings()