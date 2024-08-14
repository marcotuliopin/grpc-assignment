import grpc
import wallet_pb2
import wallet_pb2_grpc
import sys

def run():
    # Obtém os argumentos da linha de comando
    owner_key = sys.argv[1]
    server_address = sys.argv[2]

    # Cria um canal para o servidor
    with grpc.insecure_channel(server_address) as channel:
        stub = wallet_pb2_grpc.WalletServiceStub(channel)

        # Lê comandos da entrada padrão
        for line in sys.stdin:
            command = line.strip().split()

            try:
                match command[0]:
                    case 'S':
                        # Consulta o saldo
                        response = stub.GetBalance(wallet_pb2.GetBalanceRequest(owner_key=owner_key))
                        print(response.balance)
                    case 'O':
                        # Cria uma ordem de pagamento
                        amount = int(command[1])
                        response = stub.Withdraw(wallet_pb2.WithdrawRequest(owner_key=owner_key, amount=amount))
                        print(response.response)
                    case 'X':
                        # Transfere dinheiro
                        order_id = int(command[1])
                        check = int(command[2])
                        target_owner_key = command[3]
                        response = stub.Transfer(wallet_pb2.TransferRequest(order_id=order_id, check=check, owner_key=target_owner_key))
                        print(response.response)
                    case 'F':
                        # Termina a execução do servidor
                        response = stub.EndExecution(wallet_pb2.EndExecutionRequest())
                        print(response.pending_orders)
                        break
                    case _:
                        # Ignora qualquer outro comando
                        pass
            # O servidor foi interrompido
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.UNAVAILABLE:
                    break

if __name__ == '__main__':
    run()