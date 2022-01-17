# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-26 10:15:09
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-17 10:32:40


class HtlcRest:
    def __init__(self, htlc):
        self.orig_htlc = htlc
        self.incoming_channel_id = htlc.incoming_channel_id
        self.outgoing_channel_id = htlc.outgoing_channel_id
        self.incoming_htlc_id = htlc.incoming_htlc_id
        self.outgoing_htlc_id = htlc.outgoing_htlc_id
        self.event_outcome = None
        self.event_outcome_info = None
        st = htlc.__str__()
        self.timestamp = int(int(htlc.timestamp_ns) / 1e9)
        self.event_type = htlc.event_type
        if hasattr(htlc, "forward_event"):
            self.event_outcome = "forward_event"
            self.event_outcome_info = htlc.forward_event.info
        elif hasattr(htlc, "forward_fail_event"):
            self.event_outcome = "forward_fail_event"
        elif hasattr(htlc, "link_fail_event"):
            print(st)
            self.event_outcome = "link_fail_event"
            self.event_outcome_info = htlc.link_fail_event.info
        elif hasattr(htlc, "settle_event"):
            self.event_outcome = "settle_event"
