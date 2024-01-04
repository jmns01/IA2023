from Client import Client
from Node import Node
from Order import Order
from Worker import worker
from Delivery import Delivery
from Produto import Produto
from Graph import Grafo
from Vehicles import Car
from Vehicles import Motorcycle
from Vehicles import Bike
import Vehicles
import Location
import folium
from folium import plugins
import threading
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random
from matplotlib.animation import FuncAnimation
class HealthPlanet:
    def __init__(self, users=dict(), encomendas=dict(), workers=[], entrega=dict(), grafos=dict(), estafetas_por_localizacao=dict()):
        self.users = users # dicionario em que a key nome do cliente e o value o objeto cliente
        self.encomendas = encomendas # dicionario em que a key é o id da encomenda e o value o objeto order
        self.workers = workers # dicionario em que a key é o id do estafeta e o value o objeto worker
        self.entrega = entrega # dicionario em que a key é o id da entrega e o value o objeto delivery
        self.grafos = {} # dicionario em que a key é o nome da cidade e o value o objeto graph
        self.rating_needed = [] # lista de ids da entregas que ainda necessitam de ser avaliadas pelos clientes
        self.estafetas_por_localizacao = estafetas_por_localizacao # dicionário em que a key é a localização e o value uma lista de estafetas (serão sempre 5 por localização)

    def adicionar_cliente(self, username : str, password : str):
        """
        Adds a new entry to the user dictonary, and also cheks if user already exists
        :param username: The user name
        :param password: The user's password
        :return: returns void but adds new user if non existent and prints a mensage
        """
        # Verifica se o cliente já existe no dicionário
        if username not in self.users:
            # Cria uma instância de Cliente e adiciona ao dicionário
            novo_cliente = Client(username, password)
            self.users[username] = novo_cliente
            print(f"\n{username} adicionado com sucesso!")
        else:
            print("\nErro: Este nome de Cliente já está em uso.")

    def adicionar_encomenda(self, client : Client,localizacao : str, weight : float, goods : list, origem : str, destino : str, time : str) -> None:
        """
        Adds a new order to the order dictonary, cheks if it already exists and also refractors it if the total weight excedes 100kg
        :param client: A client object
        :param weight: The total weight of the order
        :param goods: The list of product objects
        :param origem: The start of the delivery
        :param destino: The end of the delivery
        :param time: The category of time
        :return: nothing but prints progress mensagens
        """
        lista_partida=[]
        if weight > 100:
            soma=0
            lista_prod=[]
            for pod in goods:
                if soma+pod.getPeso() >= 100:
                    lista_partida.append(lista_prod)
                    lista_prod=[pod]
                    soma = pod.getPeso()
                else:
                    lista_prod.append(pod)
                    soma += pod.getPeso()
            if lista_prod:
                lista_partida.append(lista_prod)
        else:
            new_order = Order(weight,localizacao, goods, origem, destino, time, client)
            #if new_order not in self.encomendas.values():
            self.encomendas[new_order.getId()] = new_order
            print(f"\nEncomenda {new_order.getId()} adicionada com sucesso!")
            # else:
            #     print("\nErro ao adicionar a encomenda")

        if len(lista_partida) > 0:
            for enc in lista_partida:
                new_order = Order(weight, enc, origem, destino, time, client)
                if new_order not in self.encomendas.values():
                    self.encomendas[new_order.getId()] = new_order
                    print(f"\nEncomenda {new_order.getId()} adicionada com sucesso!")
                else:
                    print("\nErro ao adicionar a encomenda")

    def adicionar_workers(self, nome : str) -> None:
        """
        Adds a new worker to the workers diconary, also cheks if a worker with the same name already exists
        :param nome: The name of the new worker
        :return: nothing but prints progress mensagens
        """
        if nome not in self.workers:
            new_worker = worker(nome)
            self.workers.append(new_worker)
            print(f"\nEstafeta {new_worker.getId()} adicionado com sucesso!")
        else:
            print("\nJá existe um worker com esse nome!")
            

    def adicionar_entrega(self, produtos : list[Produto], vehicle : Vehicles) -> None:
        """
        Adds a new delivery to the deliveries dictonary, cheks if there are enough workers and if the same delivery already exists
        :param produtos: A list of product object
        :return: nothing but prints progress mensagens
        """
        estafetas = self.get_estafetas_livres()
        if len(estafetas)>0:
            preco = self.calcula_preco(produtos)
            new_delivery = Delivery(produtos, estafetas[0], preco)
            print()
            if new_delivery not in self.entrega.values():
                self.entrega[new_delivery.getId()] = new_delivery
                print(f"\nEntrega {new_delivery.getId()} adicionada com sucesso!")
            else:
                print("\nErro ao adicionar a entrega")
        else:
            print("[SYS] Não exitem estafetas disponíveis!")

    def adicionar_grafo(self,nome : str,grafo : Grafo,grafob : Grafo) -> None:
        """
        Adds a new graph to the graph dictonary, also cheks if the already exist a graph of the same city
        :param nome: The location's name
        :param grafo: Graph object
        :return: nothing but prints progress mensagens
        """
        if nome not in self.grafos:
            self.grafos[nome] = (grafo,grafob)
            print(f"\nGrafo de {nome} adicionado com sucesso!")
        else:
            print("\nJá existe um grafo dessa cidade!")

    def get_encomendas_cliente(self, cliente : Client) -> list[Order]:
        """
        Gets the list of orders of a client
        :param cliente:  Client object
        :return: A list of orders
        """
        encomendas_cliente=[]
        for encomendas in self.encomendas.values():
            if encomendas.getClient() == cliente:
                encomendas_cliente.append(encomendas)
        return encomendas_cliente

    def check_if_graph_exists(self, nome : str) -> bool:
        """
        Check if graph already exists
        :param nome: Name of the location of the graph
        :return: A boolean
        """
        if nome in self.grafos:
            return True
        else: return False

    def dafault_estafetas(self) -> None:
        """
        Iniciates the default workers
        :return: None
        """
        worker_names = ["António", "Paulo", "João", "Pedro", "Joana"]

        for name in worker_names:
            estafeta = worker(name)
            self.workers.append(estafeta)

    def get_estafetas_livres(self) -> list[worker]:
        """
        Gets the list of free workers
        :return: A list of workers
        """
        lista=[]
        for estafeta in self.workers:
            if not estafeta.isOcupado():
                lista.append(estafeta)
        return lista

    def calcula_preco(self, listaProd : list[Produto]) -> float:
        """
        Gets the total price of a list of goods
        :param listaProd: A list of product objects
        :return: The total cost in a float number
        """
        preco=0.0
        for prod in listaProd:
            preco += prod.getPreco()
        return preco

    def finalizar_entrega(self, cliente : Client, entrega : Delivery, raiting : float) -> None:
        """
        Finalizes a delivery, applies the rating to the delivery and the respective worker, removes the delivery from the dictonary and alters the delivered flag in the products and orders
        :param cliente: Client object whose goods got delivered
        :param entrega: Delivery object
        :param raiting: The rating given by the client
        :return: None
        """
        entrega.setRating(raiting)
        entrega.getWorker().newRank(raiting)
        entrega.getWorker().increment_num_deliveries()
        self.entrega.pop(entrega.getId())
        cliente.add_nova_entrega(entrega)

        for prod in entrega.getProducts(): # Passar produtos a entregue
           prod.passouEntregue()

        for encomenda in self.encomendas.values(): # Passar encomenda a entregue
          if all(encomenda.getGoods().getEstado()):
              encomenda.passouEntregue()

    def get_todas_encomendas(self) -> list[Order]:
        """
        Gets the list of all orders in the system
        :return: A list of orders
        """
        todas_encomendas = list(self.encomendas.values())

        if not todas_encomendas:
            print("[SYS] Não há encomendas disponíveis no sistema.")

        return todas_encomendas

    def get_entrega_by_id(self, id : int) -> Delivery:
        """
        Gets the delivery by its id
        :param id: An integer, id of a delivery
        :return: An delivery object
        """
        return self.entrega.get(id)

    def get_entregas_por_avaliar(self, cliente : Client) -> list[Order]:
        """
        Gets the list of deliveries yet to rate by the client
        :param cliente: A client object
        :return: A list with the deliveries
        """
        entregas_por_avaliar=[]
        for ids in self.rating_needed:
            ent = self.get_entrega_by_id(ids)
            if ent.getCliente() == cliente:
                entregas_por_avaliar.append(ent)
        return entregas_por_avaliar

    def gerar_encomendas(self):

        caminho_entregas = {}
        localizacoes = []
        for id,encomenda in self.encomendas.items():
            if encomenda.getLocalizacao() not in localizacoes:
                localizacoes.append(encomenda.getLocalizacao())

        num_workers= len(self.workers)
        num_encomendas = len(self.encomendas)
        lista_destinos= {}
        total_peso = 0
        num_produtos = 0
        imediatas = 0
        urgente = 0
        normal = 0
        irrelevante = 0
        i=0
        while len(localizacoes)>0:
            lista=[]
            for id,encomenda in self.encomendas.items():
                if encomenda.getLocalizacao()==localizacoes[i]:
                    total_peso += encomenda.getWeight()
                    num_produtos += len(encomenda.getGoods())
                    lista_destinos[id] = encomenda.getDestino()
                    lista.append(encomenda)

            armazem = int(input(f"[SYS] Digite o id do nodo correspondente ao armazem da localização: {localizacoes[i]}: "))
            grafoAtual, grafoAtualb = self.grafos[localizacoes[i]]



            if(len(lista)==1):
                encomenda=lista[0]
                start = grafoAtual.get_node_by_id(armazem)
                destino = encomenda.getDestino()
                grafoAtual.calcula_heuristica_global(destino)
                pathAstar = grafoAtual.procura_aStar(start, destino, "car")
                caminhoCarroMota = grafoAtual.converte_caminho(pathAstar[0])
                custoCarro = pathAstar[1][2]
                custoMota = pathAstar[1][1]

                grafoAtualb.calcula_heuristica_global(destino)
                pathAstarb = grafoAtualb.procura_aStar(start, destino, "bike")
                caminhoBicicleta = grafoAtualb.converte_caminho(pathAstarb[0])
                custoBicicleta = pathAstarb[1][0]
                encomenda = lista[0]
                produtos=encomenda.getGoods()

                if len(produtos)==1:
                    for produto in produtos:
                        if(produto.getPeso()<=5):
                            vehicle = Bike()
                            self.adicionar_entrega(produtos, vehicle)
                            caminho_entregas[1] = self.entrega[1], [pathAstarb[0]], [caminhoBicicleta], [custoBicicleta]
                        elif(produto.getPeso()<=20):
                            vehicle = Motorcycle()
                            self.adicionar_entrega(produtos, vehicle)
                            caminho_entregas[1] = self.entrega[1], [pathAstar[0]], [caminhoCarroMota], [custoMota]
                        else:
                            vehicle = Car()
                            self.adicionar_entrega(produtos, vehicle)
                            caminho_entregas[1] = self.entrega[1], [pathAstar[0]], [caminhoCarroMota], [custoCarro]
                elif total_peso <= 5:
                    vehicle = Bike()
                    self.adicionar_entrega(produtos, vehicle)
                    caminho_entregas[1] = self.entrega[1], [pathAstarb[0]], [caminhoBicicleta], [custoBicicleta]
                elif total_peso <= 20:
                    vehicle = Motorcycle()
                    self.adicionar_entrega(produtos, vehicle)
                    caminho_entregas[1] = self.entrega[1], [pathAstar[0]], [caminhoCarroMota], [custoMota]
                elif total_peso <= 100:
                    vehicle = Car()
                    self.adicionar_entrega(produtos, vehicle)
                    caminho_entregas[1] = self.entrega[1], [pathAstar[0]], [caminhoCarroMota], [custoCarro]

            elif(len(lista)==2):
                encomenda = lista[0]
                encomenda2 = lista[1]
                soma_caminhos=0
                soma_caminhos_separados=0
                start1 = Node()
                destino1 = Node()
                pathAstar1 = []
                caminhoCarroMota1 = []
                custoCarro1 = float()
                for enc in lista:
                    start1 = grafoAtual.get_node_by_id(armazem)
                    destino1 = enc.getDestino()
                    grafoAtual.calcula_heuristica_global(destino1)
                    pathAstar1 = grafoAtual.procura_aStar(start1, destino1, "car")
                    caminhoCarroMota1 = grafoAtual.converte_caminho(pathAstar1[0])
                    custoCarro1 = pathAstar1[1][2]
                    custoMota1 = pathAstar1[1][1]
                    grafoAtualb.calcula_heuristica_global(destino1)
                    pathAstarb1 = grafoAtualb.procura_aStar(start1, destino1, "bike")
                    caminhoBicicleta1 = grafoAtualb.converte_caminho(pathAstarb1[0])
                    custoBicicleta1 = pathAstarb1[1][0]
                    soma_caminhos_separados += custoCarro1

                start = grafoAtual.get_node_by_id(armazem)
                destino = encomenda.getDestino()
                grafoAtual.calcula_heuristica_global(destino)
                pathAstar = grafoAtual.procura_aStar(start, destino, "car")
                caminhoCarroMota = grafoAtual.converte_caminho(pathAstar[0])
                custoCarro = pathAstar[1][2]
                custoMota = pathAstar[1][1]
                grafoAtualb.calcula_heuristica_global(destino)
                pathAstarb = grafoAtualb.procura_aStar(start, destino, "bike")
                caminhoBicicleta = grafoAtualb.converte_caminho(pathAstarb[0])
                custoBicicleta = pathAstarb[1][0]
                soma_caminhos += custoCarro

                start2 = destino
                destino2 = encomenda2.getDestino()
                grafoAtual.calcula_heuristica_global(destino2)
                pathAstar2 = grafoAtual.procura_aStar(start2, destino2, "car")
                caminhoCarroMota2 = grafoAtual.converte_caminho(pathAstar2[0])
                custoCarro2 = pathAstar2[1][2]
                custoMota2 = pathAstar2[1][1]
                grafoAtualb.calcula_heuristica_global(destino2)
                pathAstarb2 = grafoAtualb.procura_aStar(start2, destino2, "bike")
                caminhoBicicleta2 = grafoAtualb.converte_caminho(pathAstarb2[0])
                custoBicicleta2 = pathAstarb2[1][0]
                soma_caminhos += custoCarro2

                if soma_caminhos_separados < soma_caminhos and encomenda.getWeight()+encomenda2.getWeight() <= 100:
                    produtos_encomenda = encomenda.getGoods()
                    produtos_encomenda2 = encomenda2.getGoods()
                    produtos = []
                    produtos.extend(produtos_encomenda)
                    produtos.extend(produtos_encomenda2)
                    if encomenda.getWeight()+encomenda2.getWeight() <= 5:
                        vehicle = Bike()
                        self.adicionar_entrega(produtos, vehicle)
                        caminho_entregas[1] = self.entrega[1],[pathAstarb[0],pathAstarb2[0]], [caminhoBicicleta,caminhoBicicleta2], [custoBicicleta,custoBicicleta2]

                    elif 5 < encomenda.getWeight()+encomenda2.getWeight() <= 20:
                        vehicle = Motorcycle()
                        self.adicionar_entrega(produtos, vehicle)
                        caminho_entregas[1] = self.entrega[1], [pathAstar[0],pathAstar2[0]], [caminhoCarroMota, caminhoCarroMota2], [custoMota, custoMota2]

                    elif 20 < encomenda.getWeight()+encomenda2.getWeight() <= 100:
                        vehicle = Car()
                        self.adicionar_entrega(produtos, vehicle)
                        caminho_entregas[1] = self.entrega[1], [pathAstar[0],pathAstar2[0]], [caminhoCarroMota, caminhoCarroMota2], [custoCarro, custoCarro2]

                else:
                    produtos_encomenda = encomenda.getGoods
                    produtos_encomenda1 = encomenda2.getGoods
                    if encomenda.getWeight() <= 5 and encomenda2.getWeight() <= 5:
                        vehicle = Bike()
                        self.adicionar_entrega(produtos_encomenda, vehicle)
                        caminho_entregas[1] = self.entrega[1],[pathAstarb[0]], [caminhoBicicleta], [custoBicicleta]
                        vehicle1 = Bike()
                        self.adicionar_entrega(produtos_encomenda1, vehicle)
                        caminho_entregas[2] = self.entrega[2],[pathAstarb1[0]], [caminhoBicicleta1], [custoBicicleta1]

                    elif encomenda.getWeight() <= 5 and encomenda2.getWeight() <= 20:
                        vehicle = Bike()
                        self.adicionar_entrega(produtos_encomenda, vehicle)
                        caminho_entregas[1] = self.entrega[1], [pathAstarb[0]], [caminhoBicicleta], [custoBicicleta]
                        vehicle1 = Motorcycle()
                        self.adicionar_entrega(produtos_encomenda1, vehicle)
                        caminho_entregas[2] = self.entrega[2], [pathAstar1[0]], [caminhoCarroMota1], [custoMota1]

                    elif encomenda.getWeight() <= 5 and encomenda2.getWeight() <= 100:
                        vehicle = Bike()
                        self.adicionar_entrega(produtos_encomenda, vehicle)
                        caminho_entregas[1] = self.entrega[1], [pathAstarb[0]], [caminhoBicicleta], [custoBicicleta]
                        vehicle1 = Carro()
                        self.adicionar_entrega(produtos_encomenda1, vehicle)
                        caminho_entregas[2] = self.entrega[2], [pathAstar1[0]], [caminhoCarroMota1], [custoCarro1]

                    elif encomenda.getWeight() <= 20 and encomenda2.getWeight() <= 5:
                        vehicle = Motorcycle()
                        self.adicionar_entrega(produtos_encomenda, vehicle)
                        caminho_entregas[1] = self.entrega[1], [pathAstar[0]], [caminhoCarroMota], [custoMota]
                        vehicle1 = Bike()
                        self.adicionar_entrega(produtos_encomenda1, vehicle)
                        caminho_entregas[2] = self.entrega[2], [pathAstarb1[0]], [caminhoBicicleta1], [custoBicicleta1]

                    elif encomenda.getWeight() <= 100 and encomenda2.getWeight() <= 5:
                        vehicle = car()
                        self.adicionar_entrega(produtos_encomenda, vehicle)
                        caminho_entregas[1] = self.entrega[1], [pathAstar[0]], [caminhoCarroMota], [custoCarro]
                        vehicle1 = Bike()
                        self.adicionar_entrega(produtos_encomenda1, vehicle)
                        caminho_entregas[2] = self.entrega[2], [pathAstarb1[0]], [caminhoBicicleta1], [custoBicicleta1]

                    elif encomenda.getWeight() <= 20 and encomenda2.getWeight() <= 20:
                        vehicle = Motorcycle()
                        self.adicionar_entrega(produtos_encomenda, vehicle)
                        caminho_entregas[1] = self.entrega[1], [pathAstar[0]], [caminhoCarroMota], [custoMota]
                        vehicle1 = Motorcycle()
                        self.adicionar_entrega(produtos_encomenda1, vehicle)
                        caminho_entregas[2] = self.entrega[2], [pathAstar1[0]], [caminhoCarroMota1], [custoMota1]

                    elif encomenda.getWeight() <= 100 and encomenda2.getWeight() <= 100:
                        vehicle = Car()
                        self.adicionar_entrega(produtos_encomenda, vehicle)
                        caminho_entregas[1] = self.entrega[1], [pathAstar[0]], [caminhoCarroMota], [custoCarro]
                        vehicle1 = Car()
                        self.adicionar_entrega(produtos_encomenda1, vehicle)
                        caminho_entregas[2] = self.entrega[2],  [pathAstar1[0]], [caminhoCarroMota1], [custoCarro1]



            self.realizar_entregas(caminho_entregas,localizacoes[i])

            #localizacoes.pop(localizacoes[i])
            i+=1


    def realizar_entregas(self,caminhoEntregas,localizacao):
        thread_input = threading.Thread(target=self.thread_input_nodo_cortado, args=(localizacao,))
        thread_input.start()
        G, Gb = Location.run2(localizacao)

        entrega, nodos, caminhos, custos = caminhoEntregas[1]

        nodos_ids = [nodo.m_id for nodo in nodos[0]]
        print(nodos_ids)
        worker=entrega.getWorker()
        vehicle=entrega.getVehicle()
        # subgraph = G.subgraph(nodos_ids)
        # pos = nx.spring_layout(subgraph)  # Calcular as posições
        # nx.set_node_attributes(subgraph, pos, 'pos')  #
        #
        # # Obtém a lista de arestas que conectam os nodos na lista nodos_ids
        # edge_list = [(nodos_ids[i], nodos_ids[i + 1]) for i in range(len(nodos_ids) - 1)]
        #
        # # Desenha o subgrafo
        # nx.draw(subgraph, pos=nx.spring_layout(subgraph), with_labels=True, node_size=50)
        #
        # # Adiciona a rota como uma linha azul
        # nx.draw_networkx_edges(subgraph, pos=nx.spring_layout(subgraph), edgelist=edge_list, edge_color='b', width=2)
        #
        # # Adiciona marcadores para os nodos de entrega
        # nx.draw_networkx_nodes(subgraph, pos=nx.spring_layout(subgraph), nodelist=nodos_ids, node_color='r',
        #                        node_size=100)
        #
        # # Adiciona o veículo como um marcador
        # nx.draw_networkx_nodes(subgraph, pos=nx.spring_layout(subgraph), nodelist=[nodos_ids[0]], node_color='g',
        #                        node_size=100)
        #
        # # Adiciona um título
        # plt.title(f"Rota de entrega para o veículo {vehicle}")
        #
        # fig, ax = plt.subplots()
        # line, = ax.plot([], [], 'ro-', markersize=10)
        #
        # def update(frame):
        #     # Atualize a posição do veículo (frame a frame)
        #     current_node = nodos_ids[frame]
        #     x, y = subgraph.nodes[current_node]['pos']
        #     line.set_data(x, y)
        #     return line,
        #
        # # Número total de frames é igual ao número de nodos na rota
        # num_frames = len(nodos_ids)
        #
        # ani = FuncAnimation(fig, update, frames=num_frames, interval=1000, blit=True)
        # plt.show()


        G = nx.DiGraph()

        # Adicionar nodos e caminhos ao grafo
        for nodo in nodos:
            G.add_node(nodo)

        for caminho in caminhos:
            G.add_edge(caminho[0], caminho[1], label=caminho[2])

        # Posições para desenhar os nodos
        pos = nx.spring_layout(G)

        # Desenhar nodos
        nx.draw_networkx_nodes(G, pos, node_size=700)

        # Desenhar caminhos
        nx.draw_networkx_edges(G, pos)

        # Adicionar rótulos aos caminhos
        edge_labels = {(i, j): G[i][j]['label'] for i, j in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Adicionar rótulos aos nodos
        node_labels = {nodo: str(nodo) for nodo in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=node_labels)

        # Exibir o gráfico
        plt.show()

    def thread_input_nodo_cortado(self,localizacao):
        while True:
            try:
                grafo = int(input("[SYS] Indique qual dos grafos pretende cortar:  1: GrafoBicicleta, 2: GrafoMota, 3: GrafoCarro, 4: Exit\n Selecione ums opção: "))
                if grafo==4:
                    print(f"[SYS] Processo de cortar ruas terminado para a {localizacao}")
                    break
                grafoAtual, grafoAtualb = self.grafos(localizacao)
                if grafo==2 or grafo == 3:
                    seleciona_rua_cortar(grafoAtual)
                else:
                    seleciona_rua_cortar(grafoAtualb)
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")




    def get_encomendas_por_entregar(self, cliente : Client) -> list[Order]:
        """
        Gets a list of not delivered orders of a client
        :param cliente: A client object
        :return: A list of order objects
        """
        lista=[]
        for enc in self.encomendas.values():
            if not enc.getEstado() and enc.getClient() == cliente:
                lista.append(enc)

    def get_encomendas_entregues(self, cliente : Client) -> list[Order]:
        """
        Gets a list of delivered orders of a client
        :param cliente: A client object
        :return: A list of order objects
        """
        lista=[]
        for enc in self.encomendas.values():
            if enc.getEstado() and enc.getClient() == cliente:
                lista.append(enc)