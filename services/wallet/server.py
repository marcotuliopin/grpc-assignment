import grpc
from concurrent import futures
from threading import Event
from typing import Dict, Tuple
from sys import stdin
import wallet_pb2
import wallet_pb2_grpc

class WalletServicer(wallet_pb2_grpc.WalletServiceServicer):
    def __init__(self, _stop_ev: Event):
        self.wallets: Dict[str, int] = {}
        self.orders: Dict[int, Tuple[str, int]] = {}
        self.order_count: int = 0
        self._stop: Event = _stop_ev

    def GetBalance(self, request, context):
        if request.owner_key not in self.wallets:
            return wallet_pb2.GetBalanceResponse(balance=-1)
        balance = self.wallets[request.owner_key]
        return wallet_pb2.GetBalanceResponse(balance=balance)

    def Withdraw(self, request, context):
        # Verifica se a carteira do proprietário existe
        if request.owner_key not in self.wallets:
            # Se a carteira não existir, retorna uma resposta com -1
            response = -1
        # Verifica se a carteira tem fundos suficientes para a retirada
        elif self.wallets[request.owner_key] < request.amount:
            # Se não houver fundos suficientes, retorna uma resposta com -2
            response = -2
        else:
            # Se a carteira existir e tiver fundos suficientes, cria uma nova ordem de retirada
            # Gera um novo ID para a ordem
            order_count += 1
            response = order_count
            # Remove os fundos da carteira
            self.wallets[request.owner_key] -= request.amount
            # Adiciona a nova ordem ao dicionário de ordens
            self.orders[response] = (request.owner_key, request.amount)

        return wallet_pb2.WithdrawResponse(response=response)

    def Transfer(self, request, context):
        # Verifica se a ordem existe
        if request.order_id not in self.orders:
            # Se a ordem não existir, retorna uma resposta com -1
            return wallet_pb2.TransferResponse(response=-1)

        order_owner_key, order_amount = self.orders[request.order_id]
        # Verifica se o valor da ordem é igual ao valor de verificação fornecido na solicitação
        if order_amount != request.check:
            # Se os valores não forem iguais, retorna uma resposta com -2
            response = -2
        # Verifica se a carteira para a qual o dinheiro deve ser transferido existe
        elif request.owner_key not in self.wallets:
            # Se a carteira não existir, retorna uma resposta com -3
            response = -3
        else:
            # Realiza a transferência subtraindo o valor da ordem da carteira original e adicionando-o à carteira de destino
            response = 0 
            self.wallets[request.owner_key] += order_amount
            # Remove a ordem do dicionário de ordens
            del self.orders[request.order_id]

        return wallet_pb2.TransferResponse(response=response)

    def EndExecution(self, request, context):
        for key, value in self.wallets.items():
            print(key, value)
        self._stop.set()
        # Retorna uma resposta contendo a lista atual de saldos de todas as carteiras e o número de ordens pendentes.
        return wallet_pb2.EndExecutionResponse(pending_orders=len(self.orders))

def create_servicer():
    stop_ev = Event()
    servicer = WalletServicer(stop_ev)
    for line in stdin:
        owner_key, balance = line.strip().split()
        servicer.wallets[owner_key] = int(balance)
    return servicer, stop_ev

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer, stop_ev = create_servicer()
    wallet_pb2_grpc.add_WalletServiceServicer_to_server(servicer, server) # TODO
    server.add_insecure_port('0.0.0.0:50051') # TODO
    server.start()
    stop_ev.wait()
    server.stop()

if __name__ == '__main__':
    serve()