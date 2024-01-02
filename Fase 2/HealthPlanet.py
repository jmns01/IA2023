from Client import Client
from Node import Node
from Order import Order
from Worker import worker
from Delivery import Delivery

class HealthPlanet:
    def __init__(self, users=dict(), encomendas=dict(), workers=[], entrega=dict(), grafo=dict()):
        self.users = users # dicionario em que a key nome do cliente e o value o objeto cliente
        self.encomendas = encomendas # dicionario em que a key é o id da encomenda e o value o objeto order
        self.workers = workers # dicionario em que a key é o id do estafeta e o value o objeto worker
        self.entrega = entrega # dicionario em que a key é o id da entrega e o value o objeto delivery
        self.grafos = grafo # dicionario em que a key é o nome da cidade e o value o objeto graph

    def adicionar_cliente(self, username, password):
        # Verifica se o cliente já existe no dicionário
        if username not in self.users:
            # Cria uma instância de Cliente e adiciona ao dicionário
            novo_cliente = Client(username, password)
            self.users[username] = novo_cliente
            print("Cliente adicionado com sucesso!")
        else:
            print("Erro: Este nome de Cliente já está em uso.")

    def adicionar_encomenda(self, client, weight, goods, origem, destino, time):
        new_order = Order(weight, goods, origem, destino, time, client)

        if new_order not in self.encomendas.values():
            self.encomendas[new_order.getId()] = new_order
            print(f"Encomenda {new_order.getId()} adicionada com sucesso!")
        else:
            print("Erro ao adicionar a encomenda")

    def adicionar_workers(self, nome):
        if nome not in self.workers:
            new_worker = worker(nome)
            self.workers.append(new_worker)
            print(f"Estafeta {new_worker.getId()} adicionado com sucesso!")
        else:
            print("Já existe um worker com esse nome!")
            

    def adicionar_entrega(self, encomendas, estafeta, preco, veiculo, rating):
        new_delivery = Delivery(encomendas, estafeta, preco, veiculo, rating)

        if new_delivery not in self.entrega.value():
            self.entrega[new_delivery.getId()] = new_delivery
            print(f"Entrega {new_delivery.getId()} adicionada com sucesso!")
        else:
            print("Erro ao adicionar a entrega")

    def adicionar_grafo(self, nome, grafo):

        if nome in self.grafos:
            self.grafos[nome] = grafo
            print(f"Grafo de {nome} adicionado com sucesso!")
        else:
            print("Já existe um grafo dessa cidade!")

    def get_encomendas_cliente(self, cliente):
        encomendas_cliente=[]
        for encomendas in self.encomendas.values():
            if encomendas.getClient() == cliente:
                encomendas_cliente.append(encomendas)
        return encomendas_cliente