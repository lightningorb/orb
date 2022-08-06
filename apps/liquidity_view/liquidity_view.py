# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-23 10:44:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-06 08:17:52

import sys

from kivy.app import App

from orb.logic.pnl import pnl
from orb.misc.plugin import Plugin


class LiquidityView(Plugin):
    def main(self):
        import matplotlib.pyplot as plt

        chans = App.get_running_app().channels.channels.values()
        datas = []
        for i, c in enumerate(chans):
            if i > 10:
                break
            try:
                p = pnl(c.chan_id)
                if p:
                    datas.append(p)
            except:
                pass

        fig, axs = plt.subplots(len(datas))
        fig.suptitle("channels")

        for i, d in enumerate(datas):
            axs[i].stairs(d[0], d[1], baseline=None)
        plt.ylabel("Fees")
        plt.xlabel("Time")
        plt.gcf().autofmt_xdate()
        plt.show()
