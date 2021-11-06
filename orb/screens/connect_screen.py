from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded

class ConnectScreen(PopupDropShadow):
	@guarded
	def connect(self, address):
		from data_manager import data_man
		res = data_man.lnd.connect(address)
		print(res)

