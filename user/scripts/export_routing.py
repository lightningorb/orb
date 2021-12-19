# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-16 07:46:50
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-16 08:31:55

"""
This script exports the forwarding history to an excel sheet.
"""

import os
from openpyxl import Workbook
import arrow

from orb.dialogs.forwarding_history import get_forwarding_history

def main():

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
        for j, l in enumerate('ABCDE'):
        sheet[f"{l}{i}"] = val[j]

    fn = os.path.expanduser("~/Desktop/lnd-routing.xlsx")
    workbook.save(filename=fn)
    print(f"Done exporting to {fn}")
