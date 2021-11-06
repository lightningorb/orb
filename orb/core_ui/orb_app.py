from kivymd.app import MDApp
from orb.core_ui.main_layout import MainLayout
import data_manager
from kivy.lang import Builder
from pathlib import Path
from orb.misc.monkey_patch import do_monkey_patching
from orb.misc.conf_defaults import set_conf_defaults
from orb.audio.audio_manager import audio_manager
from orb.misc.decorators import guarded

do_monkey_patching()


class OrbApp(MDApp):
    title = "Orb"

    def load_kvs(self):
        """
        This method enables splitting up .kv files,
        currently not used.
        """
        for path in [str(x) for x in Path(".").rglob("*.kv")]:
            if any(x in path for x in ["orb.kv", 'tutes', 'dist']):
                continue
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
        settings.add_json_panel("Orb", self.config, filename="orb/misc/settings.json")

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

    @guarded
    def run(self, *args):
        super(OrbApp, self).run(*args)
