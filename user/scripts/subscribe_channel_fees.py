# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:34:14
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-06 20:35:57

from threading import Thread
from orb.misc.plugin import Plugin


Plugin().install(
    script_name="subscribe_channel_fees.py",
    menu="misc > subscribe channel fees",
    uuid="0c0d8c87-5609-468d-a41e-894aeffafbd9",
)


def main():
    def func():
        import codecs, grpc, os
        from grpc_generated import lightning_pb2 as lnrpc
        from grpc_generated import lightning_pb2_grpc as lightningstub
        from prefs import hostname, cert, macaroon, grpc_port

        os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
        ssl_creds = grpc.ssl_channel_credentials(cert())
        channel = grpc.secure_channel(f"{hostname()}:{grpc_port()}", ssl_creds)
        stub = lightningstub.LightningStub(channel)
        request = lnrpc.GraphTopologySubscription()
        for response in stub.SubscribeChannelGraph(
            request, metadata=[("macaroon", macaroon())]
        ):
            print(response)

    Thread(target=func).start()
