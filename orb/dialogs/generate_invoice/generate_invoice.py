# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 11:14:48
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-09 10:20:12

import io

from kivy.core.image import Image as CoreImage

from orb.ln import Ln
from orb.misc.decorators import guarded
from orb.components.popup_drop_shadow import PopupDropShadow


try:
    import qrcode
    from PIL import Image as PilImage
except:
    pass


class GenerateInvoice(PopupDropShadow):
    def open(self, *args):
        super(GenerateInvoice, self).open(*args)

    @guarded
    def generate(self, satoshis: str):
        ad = Ln().generate_invoice(amount=int(satoshis))
        self.ids.address.text = ad[0]
        imgIO = io.BytesIO()
        qr = qrcode.make(ad[0])
        qr.save(imgIO, ext="png")
        imgIO.seek(0)
        imgData = io.BytesIO(imgIO.read())
        self.ids.img.texture = CoreImage(imgData, ext="png").texture
        self.ids.img.reload()
