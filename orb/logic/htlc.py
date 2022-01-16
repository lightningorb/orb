# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-16 09:47:01
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-16 13:12:06

from orb.misc.prefs import is_rest
from orb.misc.prefs import is_grpc

from orb.logic.htlc_grpc import HtlcGrpc
from orb.logic.htlc_rest import HtlcRest


class Htlc:
    @staticmethod
    def init(lnd_htlc):
        if is_rest():
            return HtlcRest(lnd_htlc)
        if is_grpc():
            return HtlcGrpc(lnd_htlc)
