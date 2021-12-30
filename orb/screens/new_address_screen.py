# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-31 06:18:58

import io

from kivy.core.image import Image as CoreImage

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.lnd import Lnd


try:
    import qrcode
    from PIL import Image as PilImage
except:
    pass


class NewAddress(PopupDropShadow):
    def __init__(self, *args, **kwargs):
        super(NewAddress, self).__init__()
        ad = Lnd().new_address().address
        self.ids.address.text = ad
        imgIO = io.BytesIO()
        qr = qrcode.make(ad)
        qr.save(imgIO, ext="png")
        imgIO.seek(0)
        imgData = io.BytesIO(imgIO.read())
        self.ids.img.texture = CoreImage(imgData, ext="png").texture
        self.ids.img.reload()
