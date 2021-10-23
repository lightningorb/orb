from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from decorators import guarded

class ConnectScreen(Popup):
	@guarded
	def connect(self, address):
		from data_manager import data_man
		res = data_man.lnd.connect(address)
		print(res)

