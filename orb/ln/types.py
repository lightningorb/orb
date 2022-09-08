# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-06 14:44:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-08 17:13:30

import json
from orb.misc.auto_obj import dict2obj


class PrintableType:
    def __str__(self):
        try:
            return self.toJSON()
        except:
            return ""

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def todict(self):
        return self.__dict__


class ChainTransaction(PrintableType):
    def __init__(self, impl, tx):
        self.txid = None
        if hasattr(tx, "txid"):
            self.txid = tx.txid
        else:
            self.error = "no txid. Are there sufficient funds?"


class Info(PrintableType):
    def __init__(self, impl, **kwargs):
        self.alias = kwargs["alias"]
        self.identity_pubkey: str = ""
        self.color: str = ""
        self.block_height: str = ""
        self.network: str = ""
        self.version: str = ""
        self.num_peers: int = 0
        self.num_pending_channels: int = 0
        self.num_active_channels: int = 0
        self.num_inactive_channels: int = 0

        if impl == "lnd":
            self.identity_pubkey = kwargs["identity_pubkey"]
            self.color = kwargs["color"].replace("#", "")
            self.block_height = kwargs["block_height"]
            self.network = ("mainnet", "testnet")[kwargs["testnet"]]
        elif impl == "cln":
            self.identity_pubkey = kwargs["id"]
            self.color = str(kwargs["color"]).replace("#", "")
            self.block_height = kwargs["blockheight"]
            self.network = kwargs["network"]
        common = [
            "version",
            "num_peers",
            "num_pending_channels",
            "num_active_channels",
            "num_inactive_channels",
        ]
        for c in common:
            setattr(self, c, kwargs[c])


class ForwardingEvents(PrintableType):
    def __init__(self, impl, fwd):
        self.forwarding_events = []
        self.last_offset_index: int = 0
        if impl == "lnd":
            self.last_offset_index = fwd.last_offset_index

        name = dict(lnd="forwarding_events", cln="listForwards")

        for e in getattr(fwd, name[impl]):
            self.forwarding_events.append(ForwardingEvent(impl=impl, e=e))


class PaymentEvent(PrintableType):
    def __init__(self, impl, e):
        self.creation_date: int = 0
        self.creation_time_ns: int = 0
        self.failure_reason: str = ""
        self.fee: int = 0
        self.fee_msat: int = 0
        self.fee_sat: int = 0
        self.htlcs = None
        self.payment_hash: str = ""
        self.payment_index: int = 0
        self.payment_preimage: str = ""
        self.payment_request: str = ""
        self.status: str = ""
        self.value: int = 0
        self.value_msat: int = 0
        self.value_sat: int = 0
        self.total_fees_msat: int = 0

        if impl == "lnd":
            self.creation_date = e.creation_date
            self.creation_time_ns = e.creation_time_ns
            self.failure_reason = e.failure_reason
            self.fee = e.fee
            self.fee_msat = e.fee_msat
            self.fee_sat = e.fee_sat
            self.htlcs = e.htlcs
            self.payment_hash = e.payment_hash
            self.payment_index = e.payment_index
            self.payment_preimage = e.payment_preimage
            self.payment_request = e.payment_request
            self.status = e.status
            self.value = e.value
            self.value_msat = e.value_msat
            self.value_sat = e.value_sat
            self.total_fees_msat = e.fee_msat
        elif impl == "cln":
            self.creation_date = e.created_at
            self.creation_time_ns = e.created_at * 1000
            self.payment_request = ""
            self.status = "SUCCEEDED"
            self.value_msat = e.msatoshi
            self.value_sat = e.msatoshi // 1000
            self.fee = (e.msatoshi_sent - e.msatoshi) // 1000
            self.fee_sat = (e.msatoshi_sent - e.msatoshi) // 1000
            self.fee_msat = e.msatoshi_sent - e.msatoshi
            self.payment_hash = e.payment_hash
            self.payment_preimage = e.payment_preimage
            self.total_fees_msat = e.msatoshi_sent - e.msatoshi


class PaymentEvents(PrintableType):
    def __init__(self, impl, index_offset, max_payments, fwd):
        self.payments = []
        self.last_index_offset: int = 0
        if impl == "lnd":
            self.last_index_offset = fwd.last_index_offset
        elif impl == "cln":
            self.last_index_offset = index_offset + 1 + len(fwd)
        for f in fwd:
            self.payments.append(PaymentEvent(impl=impl, e=f))


class ForwardingEvent(PrintableType):
    def __init__(self, impl, e):
        self.amt_in: int = 0
        self.amt_in_msat: int = 0
        self.amt_out: int = 0
        self.amt_out_msat: int = 0
        self.chan_id_in: int = 0
        self.chan_id_out: int = 0
        self.fee: int = 0
        self.fee_msat: int = 0
        self.timestamp: int = 0
        self.timestamp_ns: int = 0

        if impl == "lnd":
            self.amt_in = e.amt_in
            self.amt_in_msat = e.amt_in_msat
            self.amt_out = e.amt_out
            self.amt_out_msat = e.amt_out_msat
            self.chan_id_in = e.chan_id_in
            self.chan_id_out = e.chan_id_out
            self.fee = e.fee
            self.fee_msat = e.fee_msat
            self.timestamp = e.timestamp
            self.timestamp_ns = e.timestamp_ns

        elif impl == "cln":
            self.amt_in = e.in_msatoshi // 1000
            self.amt_in_msat = e.in_msatoshi
            self.amt_out = e.out_msatoshi // 1000
            self.amt_out_msat = e.out_msatoshi
            self.chan_id_in = e.in_channel
            self.chan_id_out = e.out_channel
            self.fee = e.fee // 1000
            self.fee_msat = e.fee
            self.timestamp = int(e.resolved_time)
            self.timestamp_ns = e.resolved_time * 1000


class Balance(PrintableType):
    confirmed_balance: int
    total_balance: str
    unconfirmed_balance: str

    def __init__(self, impl, **kwargs):
        if impl == "lnd":
            self.confirmed_balance = kwargs["confirmed_balance"]
            self.total_balance = kwargs["total_balance"]
            self.unconfirmed_balance = kwargs["unconfirmed_balance"]
        elif impl == "cln":
            self.confirmed_balance = kwargs["confBalance"]
            self.total_balance = kwargs["totalBalance"]
            self.unconfirmed_balance = kwargs["unconfBalance"]


class LocalRemoteBal(PrintableType):
    local_balance: int
    remote_balance: int
    pending_balance: int
    inactive_balance: int

    def __init__(self, impl, **kwargs):
        if impl == "lnd":
            self.local_balance = kwargs["local_balance"]
            self.remote_balance = kwargs["remote_balance"]
            self.pending_balance = kwargs["pending_balance"]
            self.inactive_balance = kwargs["inactive_balance"]
        elif impl == "cln":
            self.local_balance = kwargs["localBalance"]
            self.remote_balance = kwargs["remoteBalance"]
            self.pending_balance = kwargs["pendingBalance"]
            self.inactive_balance = kwargs["inactiveBalance"]


class Policy(PrintableType):
    fee_rate_milli_msat: int
    fee_base_msat: int
    time_lock_delta: int
    max_htlc_msat: int
    min_htlc: int

    def __init__(self, impl, **kwargs):
        if impl == "lnd":
            self.fee_rate_milli_msat = kwargs["fee_rate_milli_msat"]
            self.fee_base_msat = kwargs["fee_base_msat"]
            self.time_lock_delta = kwargs["time_lock_delta"]
            self.max_htlc_msat = kwargs["max_htlc_msat"]
            self.min_htlc = kwargs["min_htlc"]
        elif impl == "cln":
            self.fee_rate_milli_msat = kwargs["fee_per_millionth"]
            self.fee_base_msat = kwargs["base_fee_millisatoshi"]
            self.time_lock_delta = kwargs["delay"]
            self.max_htlc_msat = int(kwargs["htlc_maximum_msat"][:-4])
            self.min_htlc = int(kwargs["htlc_minimum_msat"][:-4])


class PaymentRequest(PrintableType):
    def __init__(self, bolt11: str, impl: str, **kwargs):
        self.bolt11: str = bolt11
        self.destination: str = ""
        self.num_satoshis: int = 0
        self.num_msat: int = 0
        self.cltv_expiry: int = 0
        self.timestamp: int = 0
        self.expiry: int = 0
        self.description: str = ""
        self.payment_addr: str = ""
        self.payment_hash: str = ""
        self.payment_request: str = ""

        if impl == "lnd":
            self.destination = kwargs["destination"]
            self.num_satoshis = int(kwargs["num_satoshis"])
            self.num_msat = int(kwargs["num_msat"])
            self.cltv_expiry = kwargs["cltv_expiry"]
            self.timestamp = kwargs["timestamp"]
            self.payment_addr = kwargs["payment_addr"]

        elif impl == "cln":
            self.destination = kwargs["payee"]
            self.num_satoshis = int(int(kwargs["msatoshi"]) / 1000)
            self.num_msat = int(kwargs["msatoshi"])
            self.cltv_expiry = kwargs["min_final_cltv_expiry"]
            self.timestamp = kwargs["created_at"]
            self.payment_secret = kwargs["payment_secret"]

        for c in ["expiry", "description", "payment_hash"]:
            if c in kwargs:
                setattr(self, c, kwargs[c])


class NodeInfo(PrintableType):
    alias: str
    identity_pubkey: str
    last_update: int

    def __init__(self, impl, **kwargs):
        if impl == "lnd":
            self.alias = kwargs["node"]["alias"]
            self.identity_pubkey = kwargs["node"]["pub_key"]
            self.last_update = kwargs["node"]["last_update"]
            self.addresses = [
                dict2obj(dict(addr=x.addr)) for x in kwargs["node"]["addresses"]
            ]
        elif impl == "cln":
            self.alias = kwargs["alias"]
            self.identity_pubkey = kwargs["nodeid"]
            self.last_update = kwargs["last_timestamp"]
            self.addresses = [
                dict2obj(dict(addr=f"{x.address}:{x.port}"))
                for x in kwargs["addresses"]
            ]


class Route(PrintableType):
    def __init__(self, impl, total_amt, route):
        self.total_amt: int = 0
        self.total_amt_msat: int = 0
        self.total_fees_msat: int = 0
        self.total_fees: int = 0
        self.hops: list = []
        self.original = None

        if impl == "lnd":
            self.original = route
            self.total_amt = total_amt
            self.total_amt_msat = total_amt * 1000
            self.total_fees_msat = route.total_fees_msat if route else 0
            self.total_fees = self.total_fees_msat // 1000
            self.hops = route.hops if route else []
        elif impl == "cln":
            self.original = route.todict()
            self.total_amt = total_amt
            self.total_amt_msat = total_amt * 1000
            self.total_fees_msat = route.route[0].msatoshi - route.route[-1].msatoshi
            self.total_fees = self.total_fees_msat // 1000
            self.hops = []
            if hasattr(route, "route"):
                for hop in route.route:
                    self.hops.append(
                        dict2obj(
                            dict(
                                amp_record=None,
                                mpp_record=None,
                                direction=hop.direction,
                                chan_id=hop.channel,
                                pub_key=hop.id,
                                tlv_payload=hop.style == "tlv",
                                amt_to_forward=hop.msatoshi // 1000,
                                amt_to_forward_msat=hop.msatoshi,
                                chan_capacity=0,
                                custom_records={},
                                expiry=0,
                                fee=(hop.msatoshi - self.total_amt_msat) / 1000,
                                fee_msat=hop.msatoshi - self.total_amt_msat,
                                metadata="",
                            )
                        )
                    )


class SendPaymentResponse(PrintableType):
    def __init__(self, impl, response):
        self.original: list = []
        self.failure = dict2obj(dict(code=0, failure_source_index=-1))
        self.code_map = {4103: 15, 16394: 18, 16399: 1, 24579: 16, 4108: 12, 4109: 13}
        if impl == "lnd":
            self.original = response
            if hasattr(response, "failure") and response.failure:
                self.failure.code = response.failure.code
                self.failure.failure_source_index = (
                    response.failure.failure_source_index
                )
        elif impl == "cln":
            self.original = response
            if hasattr(response, "error") and response.error:
                if not hasattr(response.error, "data"):
                    pass
                if response.error.data.failcode not in self.code_map:
                    print(
                        f"code {response.error.data.failcode} ({response.error.data.failcodename}) not in map"
                    )
                    assert False
                self.failure.code = self.code_map[response.error.data.failcode]
                self.failure.failure_source_index = response.error.data.erring_index


class Peer(PrintableType):
    def __init__(self, impl, p):
        self.pub_key: str = ""
        if impl == "lnd":
            self.pub_key = p.pub_key
        elif impl == "cln":
            self.pub_key = p.id


class Peers(PrintableType):
    def __init__(self, impl, response):
        self.original = response
        self.peers: list = [Peer(impl, x) for x in response.peers]


class HTLC(PrintableType):
    def __init__(self, impl, p):
        if impl == "lnd":
            htlc = p
            self.incoming_channel_id = htlc.incoming_channel_id
            self.outgoing_channel_id = htlc.outgoing_channel_id
            self.incoming_htlc_id = htlc.incoming_htlc_id
            self.outgoing_htlc_id = htlc.outgoing_htlc_id
            self.timestamp = int(int(htlc.timestamp_ns) / 1e9)
            self.event_type = htlc.event_type
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
        elif impl == "cln":
            e_name = next(iter(p.todict().keys()))
            e = getattr(p, e_name)
            self.incoming_channel_id = None
            self.outgoing_channel_id = None
            if e_name == "sendpay_failure":
                self.event_outcome = "settle_event"
                # TODO:
                # sadly we need this information: which what route did this HTLC take?
                self.outgoing_channel_id = None  # e.data.erring_channel
                self.incoming_htlc_id = e.data.payment_hash[:5]
                self.outgoing_htlc_id = e.data.payment_hash[:5]
                if e.data.failcodename == "WIRE_TEMPORARY_CHANNEL_FAILURE":
                    self.set_fail_event(name=e_name, wire="TEMPORARY_CHANNEL_FAILURE")
                return
            if hasattr(e, "in_channel"):
                self.incoming_channel_id = e.in_channel
            if hasattr(e, "out_channel"):
                self.outgoing_channel_id = e.out_channel
            self.incoming_htlc_id = e.payment_hash[:5]
            self.outgoing_htlc_id = e.payment_hash[:5]
            if hasattr(e, "received_time"):
                self.timestamp = e.received_time
            self.event_type = next(iter(e_name.split("_"))).upper()
            if self.event_type == "SENDPAY":
                self.event_type = "SEND"
            self.event_outcome = ""
            if e_name == "forward_event":
                if e.status == "failed":
                    self.set_fail_event(e_name)
                    self.event_outcome = "forward_fail_event"
                if e.status == "settled":
                    self.event_outcome = "settle_event"
                self.set_event_outcome_info(e)
            elif e_name == "forward_event" and e.status == "failed":
                self.set_fail_event(e_name)
                self.event_outcome = "link_fail_event"
                self.set_event_outcome_info(e)

    def set_fail_event(self, name, wire="unknown", string="unknown", detail="unknown"):
        obj = dict(
            wire_failure=wire,
            failure_string=string,
            failure_detail=detail,
        )
        stem = next(iter(name.split("_")))
        setattr(self, f"{stem}_fail_event", obj)

    def set_event_outcome_info(self, e):
        self.event_outcome_info = {
            "incoming_amt_msat": e.in_msatoshi,
            "incoming_timelock": 0,
            "outgoing_amt_msat": e.out_msatoshi,
            "outgoing_timelock": 0,
        }


class ChannelHTLC(PrintableType):
    def __init__(self, impl, h):
        if impl == "cln":
            self.incoming = h.direction == "in"
            self.amount = int(h.msatoshi / 1000)
            self.htlc_index = h.payment_hash[:5]
            self.id = h.id
        elif impl == "lnd":
            self.incoming = h.incoming
            self.amount = h.amount
            self.htlc_index = h.htlc_index


class Channel(PrintableType):
    def __init__(self, impl, c):
        if impl == "cln":
            self.remote_pubkey = c.remote_pubkey
            self.capacity = int(c.msatoshi_total / 1000)
            self.pending_htlcs = [ChannelHTLC(impl=impl, h=x) for x in c.htlcs]
            total_pending_out = sum(
                x.amount for x in self.pending_htlcs if not x.incoming
            )
            total_pending_in = sum(x.amount for x in self.pending_htlcs if x.incoming)
            self.local_balance = int(c.msatoshi_to_us / 1000) - total_pending_out
            self.remote_balance = int((c.msatoshi_total - c.msatoshi_to_us) / 1000)
            self.channel_point = c.funding_txid
            self.total_satoshis_sent = 0
            self.total_satoshis_received = 0
            self.initiator = c.opener == "local"
            self.commit_fee = 0
            self.unsettled_balance = 0
            self.active = True
            self.chan_id = c.short_channel_id
        elif impl == "lnd":
            self.remote_pubkey = c.remote_pubkey
            self.capacity = c.capacity
            self.pending_htlcs = [ChannelHTLC(impl=impl, h=x) for x in c.pending_htlcs]
            self.local_balance = c.local_balance
            self.remote_balance = c.remote_balance
            self.channel_point = c.channel_point
            self.total_satoshis_sent = c.total_satoshis_sent
            self.total_satoshis_received = c.total_satoshis_received
            self.initiator = c.initiator
            self.commit_fee = c.commit_fee
            self.unsettled_balance = c.unsettled_balance
            self.active = c.active
            self.chan_id = str(c.chan_id)


class Invoice(PrintableType):
    def __init__(self, impl, i):
        if impl == "cln":
            self.remote_pubkey = i.remote_pubkey
        elif impl == "lnd":
            self.remote_pubkey = i.remote_pubkey
