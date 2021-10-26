from popup_drop_shadow import PopupDropShadow
import io
import data_manager
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image

try:
    import qrcode
    from PIL import Image as PilImage
except:
    pass


class NewAddress(PopupDropShadow):
    def __init__(self, *args, **kwargs):
        super(NewAddress, self).__init__()
        ad = data_manager.data_man.lnd.new_address().address
        self.ids.address.text = ad
        imgIO = io.BytesIO()
        qr = qrcode.make(ad)
        qr.save(imgIO, ext="png")
        imgIO.seek(0)
        imgData = io.BytesIO(imgIO.read())
        self.ids.img.texture = CoreImage(imgData, ext="png").texture
        self.ids.img.reload()
