from kivy.app import App


def console_output(text):
    app = App.get_running_app()
    if app and app.root:
        console = app.root.ids.sm.get_screen("console")
        console.print(text)


def toggle_chords():
    pass
