from kivymd.app import MDApp
from main_layout import MainLayout
import data_manager
import json
from kivy.lang import Builder
from pathlib import Path
from monkey_patch import do_monkey_patching
from conf_defaults import set_conf_defaults
from audio_manager import audio_manager

do_monkey_patching()


class OrbApp(MDApp):
    title = "Orb"

    def load_kvs(self):
        """
        This method enables splitting up .kv files,
        currently not used.
        """
        for path in [str(x) for x in Path(".").rglob("*.kv")]:
            if path not in ["orb.kv", "context_menu.kv", "app_menu.kv"] and "tutes" not in path and 'dist' not in path:
                Builder.load_file(path)

    def build(self):
        """
        Main build method for the app.
        """
        self.theme_cls.theme_style = "Dark"  # "Light"
        self.load_kvs()
        data_manager.data_man = data_manager.DataManager(config=self.config)
        # self.theme_cls.primary_palette = "Red"
        # self.icon = 'myicon.png'
        self.main_layout = MainLayout()
        audio_manager.set_volume()
        return self.main_layout

    def build_config(self, config):
        """
        Default config values.
        """
        set_conf_defaults(config)

    def build_settings(self, settings):
        """
        Configuration screen for the app.
        """
        settings.add_json_panel("Orb", self.config, filename="settings.json")

    def on_config_change(self, config, section, key, value):
        """
        What to do when a config value changes. TODO: needs fixing.
        Currently we'd end up with multiple LND instances for example?
        Simply not an option.
        """
        if f'{section}.{key}' == 'audio.volume':
            audio_manager.set_volume()
        if key == "tls_certificate":
            data_manager.DataManager.save_cert(value)
        # data_manager.data_man = data_manager.DataManager(config=self.config)
        self.main_layout.do_layout()
