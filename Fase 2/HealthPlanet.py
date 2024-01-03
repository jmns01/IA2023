from Client import Client
from Node import Node
from Order import Order
from Worker import worker
from Delivery import Delivery
from Produto import Produto
from Graph import Grafo

class HealthPlanet:
    def __init__(self, users=dict(), encomendas=dict(), workers=[], entrega=dict(), grafo=dict()):
        self.users = users # dicionario em que a key nome do cliente e o value o objeto cliente
        self.encomendas = encomendas # dicionario em que a key é o id da encomenda e o value o objeto order
        self.workers = workers # dicionario em que a key é o id do estafeta e o value o objeto worker
        self.entrega = entrega # dicionario em que a key é o id da entrega e o value o objeto delivery
        self.grafos = grafo # dicionario em que a key é o nome da cidade e o value o objeto graph

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
            print("\nCliente adicionado com sucesso!")
        else:
            print("\nErro: Este nome de Cliente já está em uso.")

    def adicionar_encomenda(self, client : Client, weight : float, goods : list, origem : str, destino : str, time : str) -> None:
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
        if weight > 100:
            soma=0
            lista_partida=[]
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

        for enc in lista_partida:
            new_order = Order(weight, goods, origem, destino, time, client)
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
            

    def adicionar_entrega(self, produtos : list[Produto]) -> None:
        """
        Adds a new delivery to the deliveries dictonary, cheks if there are enough workers and if the same delivery already exists
        :param produtos: A list of product object
        :return: nothing but prints progress mensagens
        """
        estafetas = self.get_estafetas_livres()
        if len(estafetas)>0:
            preco = self.calcula_preco(produtos)
            new_delivery = Delivery(encomendas, estafetas[0], preco)

            if new_delivery not in self.entrega.value():
                self.entrega[new_delivery.getId()] = new_delivery
                print(f"\nEntrega {new_delivery.getId()} adicionada com sucesso!")
            else:
                print("\nErro ao adicionar a entrega")
        else:
            print("[SYS] Não exitem estafetas disponíveis!")

    def adicionar_grafo(self, nome : str, grafo : Grafo) -> None:
        """
        Adds a new graph to the graph dictonary, also cheks if the already exist a graph of the same city
        :param nome: The location's name
        :param grafo: Graph object
        :return: nothing but prints progress mensagens
        """
        if nome in self.grafos:
            self.grafos[nome] = grafo
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
            self.workers[estafeta.getId()] = estafeta

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
        self.entrega.pop(entrega.getId())

        for prod in entrega.getProducts(): # Passar produtos a entregue
           prod.passouEntregue()

        for encomenda in self.encomendas.values(): # Passar encomenda a entregue
          if all(encomenda.getGoods().getEstado()):
              encomenda.passouEntregue()
