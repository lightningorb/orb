'''A kivy app to test building a custom lib in cython for android
'''
from kivy.app import App
from kivy.lang import Builder

import custom_lib


KV = '''
Label:
    text: app.get_custom_lib_result()
'''


class Application(App):
    def build(self):
        return Builder.load_string(KV)

    @staticmethod
    def get_custom_lib_result():
        return custom_lib.result()


if __name__ == "__main__":
    Application().run()
