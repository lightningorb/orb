# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-16 07:46:50
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-07 06:42:33

"""
This script exports the forwarding history to an excel sheet.
"""

import os
import arrow

from openpyxl import Workbook

from orb.dialogs.forwarding_history import get_forwarding_history
from orb.misc.plugin import Plugin

from kivy.app import App

Plugin().install(
    script_name="export_routing.py",
    menu="node > export routing",
    uuid="0a4f6319-4b53-4e3e-8b22-bbff0990bdab",
)


def main():

    print("main")

    workbook = Workbook()
    sheet = workbook.active

    sheet["A1"], sheet["B1"], sheet["C1"], sheet["D1"], sheet["E1"] = (
        "Date",
        "Amount",
        "Total Amount",
        "Fee",
        "Total Fee",
    )

    vals, total, total_fee = [], 0, 0

    for f in get_forwarding_history().iterator():
        total += f.amt_in
        total_fee += f.fee
        vals.append(
            [
                arrow.get(f.timestamp).format(),
                f"丰{f.amt_in:,}",
                f"丰{total:,}",
                f"丰{f.fee:,}",
                f"丰{total_fee:,}",
            ]
        )

    for i, val in enumerate(vals[::-1], start=2):
        for j, l in enumerate("ABCDE"):
            sheet[f"{l}{i}"] = val[j]

    user_data_dir = App.get_running_app().user_data_dir
    fn = os.path.expanduser(os.path.join(user_data_dir, "lnd-routing.xlsx"))
    workbook.save(filename=fn)
    print(f"Done exporting to {fn}")
