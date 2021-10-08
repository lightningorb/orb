from kivy.clock import mainthread
from kivy.uix.actionbar import ActionButton
from kivy.app import App

import data_manager

installed_scripts = []


def populate_scripts():
    @mainthread
    def delayed():
        app = App.get_running_app()
        # app.root.ids.ActionBar.ids.scripts.clear_widgets()
        try:
            scripts = data_manager.data_man.store.get("scripts")
        except:
            scripts = []
        for script in scripts:
            btn = ActionButton(text=script)
            app.root.ids.ActionBar.ids.scripts.add_widget(btn)

            def run(self, *args):
                lnd = data_manager.data_man.lnd
                exec(scripts[self.text])

            btn.bind(on_release=run)

    delayed()


def console_output(text):
    app = App.get_running_app()
    console = app.root.ids.sm.get_screen("console")
    console.print(text)
