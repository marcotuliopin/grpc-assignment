python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. wallet.proto 

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. store.proto 