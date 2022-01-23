from kivy.app import App as KivyApp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class AppDetails(BoxLayout):
    """
    The AppDetails contain further information on the app
    such as ratings, and provides the ability to install or
    uninstall the app.
    """

    app = ObjectProperty(rebind=True)

    def __init__(self, app, *args, **kwargs):
        self.app = app
        super(AppDetails, self).__init__(*args, **kwargs)

    def delete_app(self):
        print("deleting app from appstore")
        kivy_app = KivyApp.get_running_app()
        kivy_app.apps.delete_from_store(self.app)

    def install_uninstall(self):
        kivy_app = KivyApp.get_running_app()
        if self.app.installed:
            kivy_app.apps.uninstall(self.app)
            self.ids.install_button.disabled = True
        else:
            app = kivy_app.apps.install(self.app)
            self.ids.tip_button.disabled = False
            self.app = app
        kivy_app.root.ids.app_menu.close_all()
        kivy_app.root.ids.app_menu.populate_scripts()