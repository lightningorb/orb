# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-16 16:34:57

import sys
import os
import json
import codecs
from traceback import print_exc

from orb.misc.auto_obj import dict2obj
from orb.cln.cln_base import ClnBase
from google.protobuf.json_format import MessageToJson


sys.path.append("orb/lnd/grpc_generate")
sys.path.append("orb/lnd")

try:
    import grpc

    from orb.cln.grpc_generated import node_pb2
    from orb.cln.grpc_generated import node_pb2_grpc
    from orb.cln.grpc_generated import primitives_pb2
    from orb.cln.grpc_generated import primitives_pb2_grpc

except:
    print_exc()

MESSAGE_SIZE_MB = 50 * 1024 * 1024

b642hex = lambda x: codecs.encode(codecs.decode(x.encode(), "base64"), "hex").decode()


class ClnGRPC(ClnBase):
    def __init__(self, tls_certificate, server, port, macaroon):
        super(ClnGRPC, self).__init__("grpc")
        os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
        root_certificates: bytes = open("ca.pem", "rb").read()
        private_key: bytes = open("client-key.pem", "rb").read()
        certificate_chain: bytes = open("client.pem", "rb").read()

        self.credentials = grpc.ssl_channel_credentials(
            root_certificates=root_certificates,
            private_key=private_key,
            certificate_chain=certificate_chain,
        )
        self.channel = grpc.secure_channel(
            f"{server}:{port}",
            self.credentials,
            options=(("grpc.ssl_target_name_override", "cln"),),
        )
        self.stub = node_pb2_grpc.NodeStub(self.channel)
        self.version = None

    def get_info(self):
        json_obj = json.loads(
            MessageToJson(
                self.stub.Getinfo(node_pb2.GetinfoRequest()),
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        obj = dict2obj(json_obj)
        obj.id = b642hex(obj.id)
        obj.color = b642hex(obj.color)
        return obj

    def local_remote_bal(self):
        json_obj = json.loads(
            MessageToJson(
                self.stub.ListFunds(node_pb2.ListfundsRequest()),
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        obj = dict2obj(json_obj)
        pendingBalance: int = 0
        localBalance: int = 0
        remoteBalance: int = 0
        inactiveBalance: int = 0
        for c in obj.channels:
            if c.state == "ChanneldAwaitingLockin":
                pendingBalance += int(c.our_amount_msat.msat / 1000)
            elif c.state == "ChanneldNormal" and c.connected:
                localBalance += int(c.our_amount_msat.msat / 1000)
                remoteBalance += int(
                    (c.amount_msat.msat - c.our_amount_msat.msat) / 1000
                )
            elif c.state == "ChanneldNormal" and not c.connected:
                inactiveBalance += int(c.our_amount_msat.msat / 1000)

        return dict2obj(
            dict(
                localBalance=localBalance,
                remoteBalance=remoteBalance,
                inactiveBalance=inactiveBalance,
                pendingBalance=pendingBalance,
            )
        )

    def get_balance(self):
        json_obj = json.loads(
            MessageToJson(
                self.stub.ListFunds(node_pb2.ListfundsRequest()),
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        obj = dict2obj(json_obj)
        confBalance: int = 0
        unconfBalance: int = 0
        for o in obj.outputs:
            if o.status == "CONFIRMED":
                confBalance += int(o.amount_msat.msat / 1000)
            else:
                unconfBalance += int(o.amount_msat.msat / 1000)
        totalBalance: int = confBalance + unconfBalance
        return dict2obj(
            dict(
                unconfBalance=unconfBalance,
                confBalance=confBalance,
                totalBalance=totalBalance,
            )
        )

    def batch_open(self, pubkeys, amounts, sat_per_vbyte):
        return Exception("Multifund not available over GRPC")
