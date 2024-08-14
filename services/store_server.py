import sys
from threading import Event

import grpc
from concurrent import futures
import store_pb2
import store_pb2_grpc
import wallet_pb2
import wallet_pb2_grpc

class StoreServicer(store_pb2_grpc.StoreServiceServicer):
    def __init__(self, price, seller_key, wallet_server_address, _stop_ev: Event):
        self.price = price # Preço do produto
        self.seller_key = seller_key # Carteira do vendedor
        self.wallet_channel = grpc.insecure_channel(wallet_server_address) # Atributos para conexão com o servidor de carteira
        self.wallet_stub = wallet_pb2_grpc.WalletServiceStub(self.wallet_channel)
        self.balance = self.wallet_stub.GetBalance(wallet_pb2.GetBalanceRequest(owner_key=seller_key)).balance # Saldo do vendedor
        self._stop: Event = _stop_ev

    def GetPrice(self, request, context):
        return store_pb2.GetPriceResponse(price=self.price)

    def Sell(self, request, context):
        try:
            # Realiza um pedido de compra por meio de uma transferência utilizando o serviço de carteira
            response = self.wallet_stub.Transfer(wallet_pb2.TransferRequest(order_id=request.order_id, check=self.price, owner_key=self.seller_key))
            if response.response == 0:
                self.balance += self.price
        except grpc.RpcError:
            return store_pb2.SellResponse(response=-9)
        return store_pb2.SellResponse(response=response.response)

    def EndExecution(self, request, context):
        pending_orders = self.wallet_stub.EndExecution(wallet_pb2.EndExecutionRequest())
        self._stop.set()
        return store_pb2.EndExecutionResponse(seller_balance=self.balance, pending_orders=pending_orders.pending_orders)

def serve():
    # Obtém os argumentos da linha de comando
    price = int(sys.argv[1])
    port = int(sys.argv[2])
    seller_key = sys.argv[3]
    wallet_server_address = sys.argv[4]

    # Cria um servidor gRPC
    stop_ev = Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_StoreServiceServicer_to_server(StoreServicer(price, seller_key, wallet_server_address, stop_ev), server)
    server.add_insecure_port(f'0.0.0.0:{port}')
    # Inicia o servidor
    server.start()
    stop_ev.wait()
    # Finaliza a execução
    server.stop(grace=None)

if __name__ == '__main__':
    serve()