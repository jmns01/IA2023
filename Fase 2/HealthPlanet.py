from Client import Client
from Node import Node
from Order import Order
from Worker import worker

class HealthPlanet:
    def __init__(self, users=dict(), encomendas=dict(), workers=[], entrega=dict()):
        self.users = users # dicionario em que a key nome do cliente e o value o objeto cliente
        self.encomendas = encomendas # dicionario em que a key é o id da encomenda e o value o objeto order
        self.workers = workers # dicionario em que a key é o id do estafeta e o value o objeto worker
        self.entrega = entrega # dicionario em que a key é o id da entrega e o value o objeto delivery

    def adicionar_cliente(self, username, password):
        # Verifica se o cliente já existe no dicionário
        if username not in self.users:
            # Cria uma instância de Cliente e adiciona ao dicionário
            novo_cliente = Client(name=username, password=password)
            self.users[username] = novo_cliente
            print("Cliente adicionado com sucesso!")
        else:
            print("Erro: Este nome de Cliente já está em uso.")

    def adicionar_encomenda(self, client, weight, goods, origem, destino, time):
        new_order = Order(weight, goods, origem, desito, time, client)

        if new_order not in self.encomendas.values():
            self.encomendas[new_order.getId()] = new_order
            print(f"Encomenda {new_order.getId()} adicionada com sucesso!")
        else:
            print("Erro ao adicionar a encomenda")

    def adicionar_workers(self, nome):
        for worker in self.workers:
            if nome == worker.getName():
                print("Já existe um worker com esse nome!")
            else:
                new_worker = worker(nome)
                self.workers.append(new_worker)
                print(f"Estafeta {worker.getId()} adicionado com sucesso!")

    #def adicionar_entrega(self, encomendas, estafeta, preco, ):