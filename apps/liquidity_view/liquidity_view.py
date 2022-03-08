# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-23 10:44:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-03-08 10:35:10

from orb.misc.plugin import Plugin
from orb.logic.pnl import pnl
from orb.misc import data_manager
import sys


class LiquidityView(Plugin):
    def main(self):
        import matplotlib.pyplot as plt

        chans = data_manager.data_man.channels.channels.values()
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
