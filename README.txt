python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. wallet.proto 

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. store.proto 


make run_cli_banco arg1=carteira_cliente arg2=nome_do_host_do_serv_banco:5555
make run_serv_banco arg1=5555
make run_serv_loja arg1=10 arg2=6666 arg3=carteira_loja arg4=nome_do_host_do_serv_banco:5555
make run_cli_loja arg1=carteira_cliente arg2=nome_do_host_do_serv_banco:5555 arg3=nome_do_host_do_serv_loja:6666