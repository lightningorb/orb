# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-26 17:57:48
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-26 20:22:46
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        ti = TextInput()
        try:
            from kivymd.uix.boxlayout import MDBoxLayout
            import kivymd
            import peewee
            import simplejson
            from kivy_garden import graph
            import yaml
            import plyer
            import rsa
            import memoization

            mdbl = MDBoxLayout()
            ti.text = str(kivymd.__path__) + "\n"
            ti.text += str(MDBoxLayout) + "\n"
            ti.text += str(peewee) + "\n"
            ti.text += str(simplejson.__path__) + "\n"
            ti.text += str(graph.__path__) + "\n"
            ti.text += str(yaml.__path__) + "\n"
            ti.text += str(plyer.__path__) + "\n"
            ti.text += str(rsa.__path__) + "\n"
            ti.text += str(memoization.__path__) + "\n"
        except Exception as e:
            ti.text = str(e)
        main_layout.add_widget(ti)
        return main_layout


if __name__ == "__main__":
    app = MainApp()
    app.run()
