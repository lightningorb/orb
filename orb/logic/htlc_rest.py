# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-06 05:44:13
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-11 14:23:59

from orb.store.model import Htlc
from orb.store.db_meta import *


class HtlcRest(Htlc):
    def __init__(self, htlc):
        super(HtlcRest, self).__init__()
        self.incoming_channel_id = htlc.incoming_channel_id
        self.outgoing_channel_id = htlc.outgoing_channel_id
        self.incoming_htlc_id = htlc.incoming_htlc_id
        self.outgoing_htlc_id = htlc.outgoing_htlc_id
        st = htlc.__str__()
        self.timestamp = int(int(htlc.timestamp_ns) / 1e9)
        self.event_type = htlc.event_type
        print(st)
        if hasattr(htlc, "forward_event"):
            self.event_outcome = "forward_event"
            self.event_outcome_info = htlc.forward_event.info.todict()
        elif hasattr(htlc, "forward_fail_event"):
            self.event_outcome = "forward_fail_event"
            self.forward_fail_event = htlc.forward_fail_event.todict()
        elif hasattr(htlc, "link_fail_event"):
            self.link_fail_event = htlc.link_fail_event.todict()
            self.event_outcome = "link_fail_event"
            self.event_outcome_info = htlc.link_fail_event.info.todict()
        elif hasattr(htlc, "settle_event"):
            self.event_outcome = "settle_event"
            self.event_outcome_info = htlc.settle_event.todict()

    class Meta:
        db_table = "htlc"
        database = get_db(htlcs_db_name)
