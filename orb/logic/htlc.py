# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-26 10:15:09
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-27 18:50:05
try:
    from grpc_generated import router_pb2 as lnrouter
    from grpc_generated import lightning_pb2 as lnrpc
except:
    pass


import datetime
from peewee import *

from playhouse.sqlite_ext import *

from orb.store.db_meta import htlcs_db_name, get_db
from orb.misc.prefs import is_rest


class Htlc(Model):
    incoming_channel = CharField(default="")
    incoming_channel_id = IntegerField(default=0)
    incoming_channel_capacity = IntegerField(default=0)
    incoming_channel_local_balance = IntegerField(default=0)
    incoming_channel_remote_balance = IntegerField(default=0)
    incoming_channel_pending_htlcs = JSONField(
        default={"pending_in": 0, "pending_out": 0}
    )
    outgoing_channel = CharField(default="")
    outgoing_channel_id = IntegerField(default=0)
    outgoing_channel_capacity = IntegerField(default=0)
    outgoing_channel_local_balance = IntegerField(default=0)
    outgoing_channel_remote_balance = IntegerField(default=0)
    outgoing_channel_pending_htlcs = JSONField(
        default={"pending_in": 0, "pending_out": 0}
    )
    timestamp = IntegerField()
    event_type = CharField()
    event_outcome = CharField()
    event_outcome_info = JSONField(default={"pending_in": 0, "pending_out": 0})

    def __init__(self, lnd, htlc):
        super(Htlc, self).__init__()
        channels = lnd.get_channels()
        if getattr(htlc, "incoming_channel_id") != 0:
            ic = next(
                iter(c for c in channels if c.chan_id == htlc.incoming_channel_id), None
            )
            if ic:
                self.incoming_channel = lnd.get_alias_from_channel_id(
                    htlc.incoming_channel_id
                )
                self.incoming_channel_id = htlc.incoming_channel_id
                self.incoming_channel_capacity = ic.capacity
                self.incoming_channel_remote_balance = ic.remote_balance
                self.incoming_channel_local_balance = ic.local_balance
                self.incoming_channel_pending_htlcs = dict(
                    pending_in=sum(
                        int(p.amount) for p in ic.pending_htlcs if p.incoming
                    ),
                    pending_out=sum(
                        int(p.amount) for p in ic.pending_htlcs if not p.incoming
                    ),
                )
        else:
            self.incoming_channel = lnd.get_own_alias()
        if getattr(htlc, "outgoing_channel_id") != 0:
            self.outgoing_channel = lnd.get_alias_from_channel_id(
                htlc.outgoing_channel_id
            )
            self.outgoing_channel_id = htlc.outgoing_channel_id
            oc = next(
                iter(c for c in channels if c.chan_id == htlc.outgoing_channel_id), None
            )
            if oc:
                self.outgoing_channel_capacity = oc.capacity
                self.outgoing_channel_remote_balance = oc.remote_balance
                self.outgoing_channel_local_balance = oc.local_balance
                self.outgoing_channel_pending_htlcs = dict(
                    pending_in=sum(
                        int(p.amount) for p in oc.pending_htlcs if p.incoming
                    ),
                    pending_out=sum(
                        int(p.amount) for p in oc.pending_htlcs if not p.incoming
                    ),
                )
        else:
            self.outgoing_channel = lnd.get_own_alias()

        self.timestamp = int(int(htlc.timestamp_ns) / 1e9)
        if hasattr(htlc, "EventType"):
            self.event_type = self.get_enum_name_from_value(
                htlc.EventType.items(), htlc.event_type
            )
        else:
            self.event_type = htlc.event_type

        if is_rest():
            # RESTFUL HTLCs not fully implemented, so just pretend
            # these are forward_events for now
            self.event_outcome = "forward_event"
            return
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
        for item_key, item_value in descriptor_items:
            if (
                hasattr(item_value, "number")
                and item_value.number == value
                or item_value == value
            ):
                return item_key
        return None

    @staticmethod
    def get_event_info_enum_names_from_values(htlc_event):
        event_outcome_info = {}
        for f1, v1 in htlc_event.info.ListFields():
            for f2, v2 in htlc_event.info.DESCRIPTOR.fields_by_name.items():
                if f1 == v2:
                    event_outcome_info[f2] = v1
        return event_outcome_info

    class Meta:
        database = get_db(htlcs_db_name)


def create_htlcs_tables():
    db = get_db(htlcs_db_name)
    try:
        db.create_tables([Htlc])
    except:
        pass
