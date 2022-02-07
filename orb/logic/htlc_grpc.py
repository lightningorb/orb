# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-06 05:44:13
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-07 08:14:49

try:
    from grpc_generated import router_pb2 as lnrouter
    from grpc_generated import lightning_pb2 as lnrpc
except:
    pass

from orb.store.model import Htlc
from orb.misc.prefs import is_rest
from orb.store.db_meta import *


class HtlcGrpc(Htlc):
    def __init__(self, htlc):
        super(HtlcGrpc, self).__init__()

        if htlc.incoming_channel_id:
            self.incoming_channel_id = htlc.incoming_channel_id
            self.incoming_htlc_id = htlc.incoming_htlc_id
        if htlc.outgoing_channel_id:
            self.outgoing_channel_id = htlc.outgoing_channel_id
            self.outgoing_htlc_id = htlc.outgoing_htlc_id

        self.timestamp = int(int(htlc.timestamp_ns) / 1e9)
        self.event_type = self.get_enum_name_from_value(
            htlc.EventType.items(), htlc.event_type
        )

        self.event_outcome = self.get_enum_name_from_value(
            htlc.DESCRIPTOR.fields_by_name.items(), htlc.ListFields()[-1][0].number
        )

        if self.event_outcome == "link_fail_event":
            self.wire_failure = self.get_enum_name_from_value(
                lnrpc.Failure.FailureCode.items(), htlc.link_fail_event.wire_failure
            )
            self.failure_detail = self.get_enum_name_from_value(
                lnrouter.FailureDetail.items(), htlc.link_fail_event.failure_detail
            )
            self.failure_string = htlc.link_fail_event.failure_string
            self.event_outcome_info = self.get_event_info_enum_names_from_values(
                htlc.link_fail_event
            )
        elif self.event_outcome == "forward_event":
            self.event_outcome_info = self.get_event_info_enum_names_from_values(
                htlc.forward_event
            )

    @staticmethod
    def get_enum_name_from_value(descriptor_items, value):
        return next(
            iter(
                item_key
                for item_key, item_value in descriptor_items
                if hasattr(item_value, "number")
                and item_value.number == value
                or item_value == value
            ),
            None,
        )

    @staticmethod
    def get_event_info_enum_names_from_values(htlc_event):
        event_outcome_info = {}
        for f1, v1 in htlc_event.info.ListFields():
            for f2, v2 in htlc_event.info.DESCRIPTOR.fields_by_name.items():
                if f1 == v2:
                    event_outcome_info[f2] = v1
        return event_outcome_info

    class Meta:
        db_table = "htlc"
        database = get_db(htlcs_db_name)
