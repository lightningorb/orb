# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-20 11:23:01
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-18 17:56:15

from time import sleep
from traceback import format_exc

from peewee import fn
from orb.logic.lnurl import *
from orb.core.stoppable_thread import StoppableThread
from orb.store.db_meta import invoices_db_name
from orb.misc.decorators import db_connect
from orb.ln import Ln


class LNUrlInvoiceGenerator(StoppableThread):
    def __init__(
        self,
        url: str,
        total_amount_sat: int,
        chunks: int,
        num_threads: int,
        rate_limit: int,
        ln: Ln = None,
        wait: bool = True,
    ):
        self.total_amount_sat: int = total_amount_sat
        self.chunks: int = chunks
        self.chunk_size: int = int(total_amount_sat / chunks)
        self.invoices = set([])
        self.num_threads: int = num_threads
        self.url: str = url
        self.rate_limit: str = rate_limit
        self.ln = ln
        self.wait: bool = wait
        super(LNUrlInvoiceGenerator, self).__init__()

    def paid_everything(self):
        return self.total_amount_paid() >= self.total_amount_sat

    def total_amount_paid(self):
        from orb.store import model

        return (
            model.Invoice()
            .select(fn.SUM(model.Invoice.num_satoshis))
            .where(
                model.Invoice.paid == True,
                model.Invoice.raw.in_(self.invoices),
            )
            .scalar()
        ) or 0

    def total_amount_left_to_pay(self):
        return self.total_amount_sat - self.total_amount_paid()

    def total_amount_unpaid_invoices(self):
        from orb.store import model

        return (
            model.Invoice()
            .select(fn.SUM(model.Invoice.num_satoshis))
            .where(
                model.Invoice.paid == False,
                model.Invoice.raw.in_(self.invoices),
            )
            .scalar()
        ) or 0

    def num_usable_invoices(self):
        from orb.store import model

        return (
            len(
                model.Invoice()
                .select()
                .where(
                    model.Invoice.expired() == False,
                    model.Invoice.paid == False,
                    model.Invoice.raw.in_(self.invoices),
                )
            )
            or 0
        )

    def ingest_invoice(self, line):
        from orb.store import model

        req = self.ln.decode_payment_request(line)
        invoice = model.Invoice(
            raw=line,
            destination=req.destination,
            num_satoshis=req.num_satoshis,
            timestamp=req.timestamp,
            expiry=req.expiry,
            description=req.description,
        )
        invoice.save()
        self.invoices.add(invoice.raw)

    @db_connect(invoices_db_name)
    def run(self, *_):
        print("run")
        while not self.stopped():
            print(".")
            paid_everything = self.total_amount_paid() >= self.total_amount_sat
            print(f"total paid:      {self.total_amount_paid():_}")
            print(f"total due:       {self.total_amount_sat:_}")
            print(f"paid_everything: {paid_everything}")
            if paid_everything:
                self.stop()
            num_inv_to_complete = max(
                int(self.total_amount_left_to_pay() / self.chunk_size)
                - self.num_usable_invoices(),
                0,
            )
            num_inv_to_fill_threads = self.num_threads - self.num_usable_invoices()
            num_inv_to_create = min(num_inv_to_complete, num_inv_to_fill_threads)
            for i in range(num_inv_to_create):
                try:
                    rurl = get_callback_url(self.chunk_size, self.url)
                    req = requests.get(rurl)
                    if req.status_code == 200:
                        resp = req.json()
                        if "pr" in resp:
                            line = resp["pr"]
                            print(line)
                            self.ingest_invoice(line)
                        else:
                            print(resp)
                    else:
                        print(req.text)
                except Exception as e:
                    print(e)
                    print(format_exc())
                sleep(self.rate_limit)
            if self.wait:
                sleep(5)
            else:
                break
