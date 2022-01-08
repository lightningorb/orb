upgrade:
	curl -o lightning.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/lightning.proto
	python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. lightning.proto
	curl -o router.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/routerrpc/router.proto
	python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. router.proto

req:
	pip3 install grpcio grpcio-tools googleapis-common-protos
	git clone https://github.com/googleapis/googleapis.git