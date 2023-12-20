import math
from queue import Queue
import random
import networkx as nx  
import matplotlib.pyplot as plt

from Node import Node

import sys

sys.setrecursionlimit(5000)  # Adjust the limit accordingly

class Grafo:

    def __init__(self, directed=False, nodes=[], graph={}, edges=[]):
        self.m_directed = directed
        self.m_nodes = nodes # lista de nodos
        self.m_graph = graph # dicionario para armazenar os nodos e arestas, key é um nodo e value um par: (nodo destino, custo)
        self.m_edges = edges # lista de ruas
        self.m_h = []  # lista de dicionarios para posterirmente armazenar as heuristicas para cada nodo -< pesquisa informada

    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node" + str(key) + ": " + str(self.m_graph[key]) + "\n"
        return out
    
    def get_node_by_id(self, id):
        """
        Get the node that has the identifier id
        :param id: The id of the node
        :return: Returns a Node object or None if there is no node with that id
        """
        for node in self.m_nodes:
            if(node.m_id == id):
                return node
        return None
    
    def get_edge_by_nodes(self, origem, destino):
        """
        Get the edge that is formed by the 2 input nodes
        :param origem: The node of origin
        :param destino: the node of destinations
        :return: The edge object that is formed by the 2 input nodes or None if there is not such edge
        """

        for edge in self.m_edges:
            if edge.getOrigem() == origem.getId() and edge.getDestino() == destino.getId():
                return edge
        return None

    def converte_caminho(self, path):
        """
        Converts the output of the search algorithms to a readable version (Replaces nodes id's with street names)
        :param path: The path returned by the search algorithms which is a list of nodes
        :return: A list of strings, that represent the path
        """
        i=0
        newpath = []
        prev_edge_name = None
        while (i + 1) < len(path):
            edge_name = self.get_edge_by_nodes(path[i], path[i + 1]).getName()
            roundabout = self.get_edge_by_nodes(path[i], path[i + 1]).getRoundabout()

            if str(edge_name):
                if '(' in str(edge_name):
                    edge_name, _ = str(edge_name).split('(')
                if roundabout and "Rotunda" not in str(edge_name):
                    edge_name = f"Rotunda da Rua: {str(edge_name)}"
            elif roundabout:
                edge_name = "Rotunda"
            else:
                edge_name = self.get_edge_by_nodes(path[i], path[i + 1]).getHighway()
                edge_name = f"Highway_Type: {str(edge_name)}"

            if edge_name != prev_edge_name:
                newpath.append(str(edge_name))
                prev_edge_name = edge_name

            i += 1

        return newpath

    def imprime_arestas(self):
        """
        Prints all the connection between nodes
        :return: A list of strings containing a "pretty" text representation of the edges
        """
        lista = []
        nodes = self.m_graph.keys()
        for nodo in nodes:
            for (adj, custo) in self.m_graph[nodo]:
                lista.append(nodo + " -> " + adj + " custo: " + str(custo))
        return lista

    def getNodes(self):
        """
        Gets all the nodes of the graph
        :return: A list with all the nodes of the graph
        """
        return self.m_nodes

    def get_arc_cost(self, node1, node2): # Isto, assim como calcula_custo() vão mudar para o nosso exemplo (custo será uma fórmula que incluí tempo da viagem + poluição feita no total)
        """
        Calculates the cost of a edge between the 2 argument nodes
        :param node1: The start node object
        :param node2: The end node object
        :return: The total cost of the edge connecting the 2 nodes
        """
        custoT = math.inf
        n = node1.getId()
        a = self.m_graph[n]  # lista de arestas para aquele nodo
        for (nodo, custo, k) in a:
            if nodo == node2.getId():
                custoT = custo

        return custoT

    def calcula_custo(self, caminho):
        """
        Calculates the cost of a path for all of the current type of vehicles
        :param caminho: A list of nodes usualy returned by algorithms
        :return: A list of costs where the first index is cost for the bike, the second cost for the motorcicle and the last for car
        """
        teste = caminho
        custo = 0
        i = 0
        custos_veiculos = []
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            i = i + 1
        custos_veiculos.append(custo) # custo para bike
        custos_veiculos.append(custo + custo*0.13) # custo para moto
        custos_veiculos.append(custo + custo*0.37) # custo para carro
        return custos_veiculos

    ################################################################################
    # Procura DFS
    ####################################################################################

    def procura_DFS2(self, start, end, path=[], visited=set()): # start e end são nodos
        """
        Deph First Search algorithm adapted to our graph
        :param start: The start node object
        :param end: The end node object
        :param path: The current path taken (used for recursion)
        :param visited: A set to keep track of what nodes have been visited
        :return: A list of nodes representing the path from the start node to the end node
        """
        path.append(start)
        visited.add(start)

        if start == end:
            custoT = self.calcula_custo(path)
            return (path, custoT)
        
        if start.getId() in self.m_graph.keys():
            for(adjacente, peso, k) in self.m_graph[start.getId()]:
                nodo = self.get_node_by_id(adjacente)
                if nodo not in visited and not self.get_edge_by_nodes(start, nodo).isCortada(): # Deixar assim para ser mais eficiente (get_edge_by_node() precorre a lista de edges)
                    if self.get_edge_by_nodes(start, nodo).isTransito():
                        peso += 500 # Valor arbitrário, talvez fazer aqui algo dinâmico?
                    resultado = self.procura_DFS2(nodo, end, path, visited)
                    if resultado is not None:
                        return resultado
        path.pop()

        return None

    #####################################################
    # Procura BFS
    ######################################################

    def procura_BFS(self, start, end):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()

        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in self.m_graph[nodo_atual]:
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)



        # Reconstruir o caminho

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            custo = self.calcula_custo(path)
        return (path, custo)

    ###################################################
    # Função   getneighbours, devolve vizinhos de um nó
    ####################################################

    def getNeighbours(self, nodo):
        lista = []
        for (adjacente, peso) in self.m_graph[nodo]:
            lista.append((adjacente, peso))
        return lista

    ###############################
    #  Desenha grafo  modo grafico
    ###############################

    def desenha(self):
        ##criar lista de vertices
        lista_v = self.m_nodes
        lista_a = []
        g = nx.Graph()
        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
            for (adjacente, peso) in self.m_graph[n]:
                lista = (n, adjacente)
                # lista_a.append(lista)
                g.add_edge(n, adjacente, weight=peso)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    ##########################################################################
    #  add_heuristica   -> define heuristica para cada nodo
    ##########################################################################

    def add_heuristica(self, n, estima):
        n1 = Node(n)
        if n1 in self.m_nodes:
            self.m_h[n] = estima



    #######################################################################
    #    heuristica   -> define heuristica para cada nodo 1 por defeito....
    #    apenas para teste de pesquisa informada
    #######################################################################

    # A heuristica é calculada numa maneira pseudo bfs, começa no nodo objetivo e vai explorando os seus adjacentes somando á heuristica do seu nodo pai a heuristica do atual (tempo para percorrer do final até lá)
    def heuristica(self, destino): # destino é o nome
        dicBike = self.heurisitcas_by_vehicle(destino, 10)
        dicMoto = self.heurisitcas_by_vehicle(destino, 35)
        dicCar = self.heurisitcas_by_vehicle(destino, 50)

        self.m_h.append(dicBike)
        self.m_h.append(dicMoto)
        self.m_h.append(dicCar)

    def heurisitcas_by_vehicle(self, destino, vel):
        dic = {}
        n1 = self.get_node_by_name(destino)
        heuristica = self.calculate_time(n1.street_length, vel) # heuristica do primeiro nodo (nodo objetivo)
        dic[destino] = heuristica
        
        queue = [destino]

        while queue:
            current = queue.pop(0)
            c = self.get_node_by_name(current)
            for (adj, custo) in c.adjacent_streets:
                if adj not in dic.keys():
                    n2 = self.get_node_by_name(adj)
                    dic[adj] = dic[current] + self.calculate_time(n2.street_length, vel)
                    queue.append(adj)

        return dic

    
    def calculate_time(self, length_in_meters, speed_kmh):
        speed_ms = speed_kmh * 1000 / 3600
        time_seconds = length_in_meters / speed_ms

        return round(time_seconds, 2)

        



    ##########################################3
    #
    def calcula_est(self, estima):
        l = list(estima.keys())
        min_estima = estima[l[0]]
        node = l[0]
        for k, v in estima.items():
            if v < min_estima:
                min_estima = v
                node = k
        return node

    ##########################################
    #    A*
    ##########################################

    def procura_aStar(self, start, end):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = {start}
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}  ##  g é apra substiruir pelo peso  ???

        g[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start
        n = None
        while len(open_list) > 0:
            # find a node with the lowest value of f() - evaluation function
            calc_heurist = {}
            flag = 0
            for v in open_list:
                if n == None:
                    n = v
                else:
                    flag = 1
                    calc_heurist[v] = g[v] + self.getH(v)
            if flag == 1:
                min_estima = self.calcula_est(calc_heurist)
                n = min_estima
            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                #print('Path found: {}'.format(reconst_path))
                return (reconst_path, self.calcula_custo(reconst_path))

            # for all neighbors of the current node do
            for (m, weight) in self.getNeighbours(n):  # definir função getneighbours  tem de ter um par nodo peso
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    ###################################3
    # devolve heuristica do nodo
    ####################################

    def getH(self, nodo):
        if nodo not in self.m_h.keys():
            return 1000
        else:
            return (self.m_h[nodo])


    ##########################################
    #   Greedy
    ##########################################

    def greedy(self, start, end):
        # open_list é uma lista de nodos visitados, mas com vizinhos
        # que ainda não foram todos visitados, começa com o  start
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        open_list = set([start])
        closed_list = set([])

        # parents é um dicionário que mantém o antecessor de um nodo
        # começa com start
        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            # encontraf nodo com a menor heuristica
            for v in open_list:
                if n == None or self.m_h[v] < self.m_h[n]:
                    n = v

            if n == None:
                print('Path does not exist!')
                return None

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            # para todos os vizinhos  do nodo corrente
            for (m, weight) in self.getNeighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None
