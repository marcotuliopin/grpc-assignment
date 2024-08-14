import sys
import os
from threading import Event
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import grpc
from concurrent import futures
import store_pb2
import store_pb2_grpc
import wallet.wallet_pb2 as wallet_pb2
import wallet.wallet_pb2_grpc as wallet_pb2_grpc

class StoreServicer(store_pb2_grpc.StoreServiceServicer):
    def __init__(self, price, seller_key, wallet_server_address, _stop_ev, stop_ev: Event):
        self.price = price
        self.seller_key = seller_key
        self.wallet_channel = grpc.insecure_channel(wallet_server_address)
        self.wallet_stub = wallet_pb2_grpc.WalletServiceStub(self.wallet_channel)
        self.balance = self.wallet_stub.GetBalance(wallet_pb2.GetBalanceRequest(owner_key=seller_key)).balance
        self._stop: Event = _stop_ev

    def GetPrice(self, request, context):
        return store_pb2.GetPriceResponse(price=self.price)

    def Sell(self, request, context):
        response = self.wallet_stub.Transfer(wallet_pb2.TransferRequest(order_id=request.order_id, check=self.price, owner_key=self.seller_key))
        if response.response == 0:
            self.balance += self.price
        return store_pb2.SellResponse(status=response.response)

    def EndExecution(self, request, context):
        pending_orders = self.wallet_stub.EndExecution(wallet_pb2.EndExecutionRequest()).pending_orders
        self._stop.set()
        return store_pb2.EndExecutionResponse(seller_balance=self.balance, pending_orders=pending_orders)

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
    server.add_insecure_port(f'[::]:{port}') # TODO
    # Inicia o servidor
    server.start()
    stop_ev.wait()
    server.stop()

if __name__ == '__main__':
    serve()