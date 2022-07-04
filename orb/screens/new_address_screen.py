# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-02 12:31:35

import io

from kivy.core.image import Image as CoreImage

from orb.lnd import Lnd
from orb.misc.decorators import guarded
from orb.components.popup_drop_shadow import PopupDropShadow


try:
    import qrcode
    from PIL import Image as PilImage
except:
    pass


class NewAddress(PopupDropShadow):
    @guarded
    def open(self, *args):
        super(NewAddress, self).open(*args)
        ad = Lnd().new_address()
        print(ad)
        self.ids.address.text = ad.address
        imgIO = io.BytesIO()
        qr = qrcode.make(ad.address)
        qr.save(imgIO, ext="png")
        imgIO.seek(0)
        imgData = io.BytesIO(imgIO.read())
        self.ids.img.texture = CoreImage(imgData, ext="png").texture
        self.ids.img.reload()
