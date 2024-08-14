.PHONY: clean stubs run_serv_banco run_cli_banco run_serv_loja run_cli_loja

clean:
	rm -f services/wallet/*_pb2.py services/wallet/*_pb2_grpc.py services/wallet/__pycache__
	rm -f services/store/*_pb2.py services/store/*_pb2_grpc.py services/store/__pycache__

stubs:
	python -m grpc_tools.protoc -I./services/wallet --python_out=./services/wallet --grpc_python_out=./services/wallet ./services/wallet/wallet.proto
	python -m grpc_tools.protoc -I./services/store --python_out=./services/store --grpc_python_out=./services/store ./services/store/store.proto

run_serv_banco:
	python3 ./services/wallet/svc_banco.py $(arg1)

run_cli_banco:
	python3 ./services/wallet/cln_banco.py $(arg1) $(arg2)

run_serv_loja:
	python3 ./services/store/svc_loja.py $(arg1) $(arg2) $(arg3) $(arg4)

run_cli_loja:
	python3 ./services/store/cln_loja.py $(arg1) $(arg2) $(arg3)