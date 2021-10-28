"""
This script is a no frills way of testing the connection to an LND node.

Example invocation:

python3 test_connection.py \
	--hostname 127.0.0.1 \
	--grpc-port 10009 \
	--macaroon '~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon' \
	--cert '~/.lnd/tls.cert'

"""

import codecs, grpc, os
import grpc_generated.lightning_pb2 as lnrpc, grpc_generated.lightning_pb2_grpc as lightningstub
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--macaroon", type=str, help="path to macaroon", default='~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon')
parser.add_argument("-c", "--cert", type=str, help="path to tls certificate", default='~/.lnd/tls.cert')
parser.add_argument("-H", "--hostname", type=str, help="hostname or ip of lightning node", default='127.0.0.1')
parser.add_argument("-g", "--grpc-port", type=str, help="hostname or ip of lightning node", default='10009')
args = parser.parse_args()

macaroon = codecs.encode(open(os.path.expanduser(args.macaroon), 'rb').read(), 'hex')
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
cert = open(os.path.expanduser(args.cert), 'rb').read()

ssl_creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel(f'{args.hostname}:{args.grpc_port}', ssl_creds)
stub = lightningstub.LightningStub(channel)
request = lnrpc.GetInfoRequest()
response = stub.GetInfo(request, metadata=[('macaroon', macaroon)])

print(response)