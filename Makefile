.PHONY: clean stubs run_serv_banco run_cli_banco run_serv_loja run_cli_loja banco_stub loja_stub

all: clean stubs

clean:
	rm -rf services/*_pb2.py services/*_pb2_grpc.py services/__pycache__

stubs: banco_stub loja_stub

loja_stub: services/store_pb2.py services/store_pb2_grpc.py

services/store_pb2.py services/store_pb2_grpc.py: services/store.proto
	python3 -m grpc_tools.protoc -I./services/ --python_out=./services/ --grpc_python_out=./services ./services/store.proto

banco_stub: services/wallet_pb2.py services/wallet_pb2_grpc.py

services/wallet_pb2.py services/wallet_pb2_grpc.py: services/wallet.proto
	python3 -m grpc_tools.protoc -I./services/ --python_out=./services/ --grpc_python_out=./services ./services/wallet.proto

run_serv_banco: stubs
	python3 services/wallet_server.py $(arg1)

run_cli_banco: stubs
	python3 services/wallet_client.py $(arg1) $(arg2)

run_serv_loja: stubs
	python3 services/store_server.py $(arg1) $(arg2) $(arg3) $(arg4)

run_cli_loja: stubs
	python3 services/store_client.py $(arg1) $(arg2) $(arg3)