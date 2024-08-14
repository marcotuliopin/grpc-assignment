import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import grpc
import store_pb2
import store_pb2_grpc
import wallet.wallet_pb2 as wallet_pb2
import wallet.wallet_pb2_grpc as wallet_pb2_grpc

def run():
    # Obtém os argumentos da linha de comando
    buyer_key = sys.argv[1]
    wallet_server_address = sys.argv[2]
    store_server_address = sys.argv[3]

    # Cria um stub para o servidor da carteira
    wallet_channel = grpc.insecure_channel(wallet_server_address)
    wallet_stub = wallet_pb2_grpc.WalletServiceStub(wallet_channel)

    # Cria um stub para o servidor da loja
    store_channel = grpc.insecure_channel(store_server_address)
    store_stub = store_pb2_grpc.StoreServiceStub(store_channel)

    # Consulta o preço do produto
    price = store_stub.GetPrice(store_pb2.GetPriceRequest()).price
    print(price)

    # Lê comandos da entrada padrão
    for line in sys.stdin:
        command = line.strip()

        if command == 'C':
            # Faz a compra de um produto
            order_response = wallet_stub.Withdraw(wallet_pb2.WithdrawRequest(owner_key=buyer_key, amount=price))
            print(order_response.response)
            if order_response.response >= 0:
                sell_response = store_stub.Sell(store_pb2.SellRequest(order_id=order_response.response))
                print(sell_response.status)
        elif command == 'T':
            # Dispara a operação de término do servidor da loja
            end_execution_response = store_stub.EndExecution(store_pb2.EndExecutionRequest())
            print(end_execution_response.seller_balance, end_execution_response.pending_orders)
            break

if __name__ == '__main__':
    run()