import io
from kivy.uix.screenmanager import Screen
import data_manager
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image

try:
    import qrcode
    from PIL import Image as PilImage
except:
    pass


class NewAddressScreen(Screen):
    def on_enter(self):
        ad = data_manager.data_man.lnd.new_address().address
        self.ids.address.text = ad
        # image = Image(source="")
        imgIO = io.BytesIO()
        qr = qrcode.make(ad)
        qr.save(imgIO, ext="png")
        imgIO.seek(0)
        imgData = io.BytesIO(imgIO.read())
        self.ids.img.texture = CoreImage(imgData, ext="png").texture
        self.ids.img.reload()
