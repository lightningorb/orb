from kivy.app import App
from threading import Lock

mutex = Lock()


def console_output(text):
    mutex.acquire()
    try:
        app = App.get_running_app()
        if app and app.root:
            console = app.root.ids.sm.get_screen("console")
            console.print(text)
    finally:
        mutex.release()


def toggle_chords():
    pass
