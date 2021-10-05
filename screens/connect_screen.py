from kivy.uix.screenmanager import Screen

from data_manager import data_man


class ConnectScreen(Screen):
    def connect(self, address):
        try:
            result = data_man.lnd.connect(address)
            print(result)
        except:
            print("Maybe something went wrong")
