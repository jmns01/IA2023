import math
from queue import Queue
from queue import PriorityQueue
import heapq
import random
import networkx as nx  
import matplotlib.pyplot as plt
from fuzzywuzzy import process
import re

from Node import Node

import sys

sys.setrecursionlimit(5000)  # Adjust the limit accordingly, needed for DFS

class Grafo:

    def __init__(self, nodes=[], graph={}, edges=[]):
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
        :param id(Integer): The id of the node
        :return(Node Object): Returns a Node object or None if there is no node with that id
        """
        for node in self.m_nodes:
            if(node.m_id == id):
                return node
        return None
    
    def get_edge_by_nodes(self, origem, destino):
        """
        Get the edge that is formed by the 2 input nodes
        :param origem(Node Object): The node of origin
        :param destino(Node Object): the node of destinations
        :return: The edge object that is formed by the 2 input nodes or None if there is not such edge
        """

        for edge in self.m_edges:
            if edge.getOrigem() == origem.getId() and edge.getDestino() == destino.getId():
                return edge
        return None
    
    def get_edge_by_name(self, street):
        """
        Get the edge object by it's real-life street name or a suggestion of the possible streets wanted
        :param street(String): A street name
        :return: An edge object or a string
        """
        exact = self.get_edge_by_name_exact(street)
        if len(exact) > 0:
            return exact
        
        suggestion = self.get_edge_by_name_suggestion(street)
        return f"Rua não encontrada. \n Quereria dizer: {', '.join(suggestion)}"

    def get_edge_by_name_exact(self, street):
        """
        Get the group of the exact edges that has the same name as the string street
        :param street(String): The street name
        :return: A list with adge objects
        """
        lista=[]
        section = r'\([0-9]+\)'
        for edge in self.m_edges:
            if isinstance(edge.getName(), list):
                for names in edge.getName():
                    striped = names.split(" ")
                    last = striped[-1]
                    if names == street or (" ".join(striped[:-1]) == street and re.match(section, last)):
                        lista.append(edge)
                continue
            striped = edge.getName().split(" ")
            last = striped[-1]
            if edge.getName() == street or (" ".join(striped[:-1]) == street and re.match(section, last)):
                lista.append(edge)
        return lista
    
    def get_edge_by_name_suggestion(self, street, threshold=80):
        """
        Using the fuzzywuzzy libary to find street name with similar names as the input, it uses the Levenshtein distance to
        calculate the similarity between 2 words
        :param street(String): The name of the street
        :param threshold(Int): The precentage of similarity that is bound to be concidered a similar word
        :return: A list of the similar street names
        """
        list_of_names=[]
        for edge in self.m_edges:
            if isinstance(edge.getName(), list):
                for names in edge.getName():
                    list_of_names.append(names)
            else: list_of_names.append(edge.getName())

        suggestions = process.extract(street, list_of_names, limit=10)
        filtered_suggestions = [suggestion[0] for suggestion in suggestions if suggestion[1] >= threshold]

        return filtered_suggestions
    
    def get_intersection_node(self, edge1, edge2):
        """
        Gets the intersection between 2 edges
        :param edge1(Object Rua): A list of edges
        :param edge2(Object Rua): A list of edges
        :return: The id of a node or None
        """
        
        for edge in edge1:
            origem = edge.getOrigem()
            destino = edge.getDestino()
            for edges in edge2:
                if origem == edges.getOrigem(): return origem
                elif destino == edges.getDestino(): return destino
        return None

    def converte_caminho(self, path):
        """
        Converts the output of the search algorithms to a readable version (Replaces nodes id's with street names)
        :param path(List[Node Object]): The path returned by the search algorithms which is a list of nodes
        :return: A list of strings, that represent the path
        """
        i=0
        newpath = []
        prev_edge_name = None
        while (i + 1) < len(path):

            edge_name = self.get_edge_by_nodes(path[i], path[i + 1]).getName()
            roundabout = self.get_edge_by_nodes(path[i], path[i + 1]).getRoundabout()
            ref = self.get_edge_by_nodes(path[i], path[i + 1]).getRef()
            bridge = self.get_edge_by_nodes(path[i], path[i + 1]).getBridge()
            tunnel = self.get_edge_by_nodes(path[i], path[i + 1]).getTunnel()

            if str(edge_name):
                if '(' in str(edge_name):
                    edge_name, _ = str(edge_name).split('(')
                    edge_name = str(edge_name).rstrip()
                if roundabout and "Rotunda" not in str(edge_name):
                    edge_name = f"Rotunda da Rua: {str(edge_name)}"
                if bridge:
                    if bridge == "yes":
                        edge_name = f"{str(edge_name)} | Ponte"
                    else:
                        edge_name = f"{str(edge_name)} | Viaduto"
                if tunnel:
                    edge_name = f"{str(edge_name)} | Tunel"
            elif roundabout:
                edge_name = "Rotunda"
            elif bridge:
                if bridge == "yes":
                    edge_name = "Ponte"
                else:
                    edge_name = "Viaduto"
            elif tunnel:
                edge_name = "Tunel"
            elif ref:
                edge_name = str(ref)
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
        :param node1(Node Object): The start node object
        :param node2(Node Object): The end node object
        :return: The total cost of the edge connecting the 2 nodes
        """
        custoT = math.inf
        n = node1.getId()
        a = self.m_graph[n]  # lista de arestas para aquele nodo
        for (nodo, custo, k) in a:
            if nodo == node2.getId():
                custoT = custo

        return custoT

    def calcula_custo(self, caminho, lista_transito):
        """
        Calculates the cost of a path for all of the current type of vehicles
        :param caminho(List[Node Object]): A list of nodes usualy returned by algorithms
        :param lista_transito(List[Ruas Object]): A list of edges that had traffic in them when the algorithms passed thought them
        :return: The total cost of the path
        """
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            arc_cost = self.get_arc_cost(teste[i], teste[i + 1])
            if self.get_edge_by_nodes(teste[i], teste[i+1]) in lista_transito:
                custo += arc_cost + arc_cost*(random.uniform(0.20,0.70)) # Caso o edge teve transito este irá aumentar o custo entre 20% e 70%
            else: custo += arc_cost
            i = i + 1

        return custo

    ###########################
    #       Procura DFS       #
    ###########################

    def procura_DFS(self, start, end, path=[], visited=set(), lista_transito=[], n_nos_explorados=0): # start e end são nodos
        """
        Deph First Search algorithm adapted to our graph and circumstances
        :param start(Node Object): The current node object of the recursive call
        :param end(Node Object): The end node object
        :param path(List[Node Object]): The current path taken (used for recursion)
        :param visited(Set{Node Object}): A set to keep track of what nodes have been visited
        :param lista_transito(List[Ruas Object]): A list of edges that had traffic in them when the algorithms passed thought them
        :return: A list of nodes representing the path from the start node to the end node and the total cost pair
        """
        path.append(start)
        visited.add(start)

        if start == end:
            custoT = self.calcula_custo(path, lista_transito)
            return (path, custoT, n_nos_explorados)
        
        if start.getId() in self.m_graph.keys():
            for(adjacente, peso, k) in self.m_graph[start.getId()]:
                nodo = self.get_node_by_id(adjacente)
                if nodo not in visited and not self.get_edge_by_nodes(start, nodo).isCortada(): # Deixar assim para ser mais eficiente (get_edge_by_node() precorre a lista de edges)
                    if self.get_edge_by_nodes(start, nodo).isTransito():
                        lista_transito.append(self.get_edge_by_nodes(start, nodo))
                    resultado = self.procura_DFS(nodo, end, path, visited, lista_transito, n_nos_explorados + 1)
                    if resultado is not None:
                        return resultado
        path.pop()

        return None

    ###########################
    #       Procura BFS       #
    ###########################

    def procura_BFS(self, start, end):
        """
        Breath First search algorithm adapted to our graph and circumstances
        :param start(Node Object): The start node object
        :param end(Node Object): The end node object
        :return: A list of nodes representing the path from the start node to the end node and the total cost pair
        """
        lista_transito=[] # Lista de edges que foram passados enquanto tiveram transito (o seu custo de passagem será maior)
        n_nos_explorados=0
        visited = set()
        fila = Queue()

        fila.put(start)
        visited.add(start)

        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and not path_found:
            nodo_atual = fila.get()
            if nodo_atual == end:
                path_found = True
            
            elif nodo_atual.getId() in self.m_graph.keys():
                for (adjacente, peso, k) in self.m_graph[nodo_atual.getId()]:
                    nodo = self.get_node_by_id(adjacente)
                    if nodo not in visited and not self.get_edge_by_nodes(nodo_atual, nodo).isCortada():
                        if self.get_edge_by_nodes(nodo_atual, nodo).isTransito():
                            lista_transito.append(self.get_edge_by_nodes(nodo_atual, nodo))
                        fila.put(nodo)
                        parent[nodo] = nodo_atual
                        visited.add(nodo)
                        n_nos_explorados += 1

        path = []
        custo = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            custo = self.calcula_custo(path, lista_transito)
        return (path, custo, n_nos_explorados)
    
    #####################################
    #       Procura Bidirectional       #
    #####################################

    def procura_bidirecional(self, start, end):
        """
        Bidirectional Search adapted to our graph and circumstances
        :param start(Node Object): The start node object
        :param end(Node Object): The end node object
        :return: A list of nodes representing the path from the start node to the end node and the total cost pair
        """
        lista_transito=[]
        path_found = False
        n_nos_explorados=0

        forward_queue = Queue()
        forward_visited = set()
        forward_parent = dict()

        backward_queue = Queue()
        backward_visited = set()
        backward_parent = dict()
        
        forward_queue.put(start)
        backward_queue.put(end)

        forward_visited.add(start)
        backward_visited.add(end)

        forward_parent[start] = None
        backward_parent[end] = None

        meeting_point = None

        while (not forward_queue.empty() and not backward_queue.empty()) and not path_found:
            current_forward = forward_queue.get()
            current_backward = backward_queue.get()
            intersection = forward_visited.intersection(backward_visited)

            if intersection:
                path_found = True
                meeting_point = intersection.pop()
                
            if current_forward.getId() in self.m_graph.keys():
                for (neighbor_fwd, cost_fwd, k) in self.m_graph[current_forward.getId()]:
                    node_fwd = self.get_node_by_id(neighbor_fwd)
                    if node_fwd not in forward_visited and not self.get_edge_by_nodes(current_forward, node_fwd).isCortada():
                        edge_fwd = self.get_edge_by_nodes(current_forward, node_fwd)
                        if edge_fwd.isTransito():
                            lista_transito.append(edge_fwd)
                        forward_queue.put(node_fwd)
                        forward_parent[node_fwd] = current_forward
                        forward_visited.add(node_fwd)
                        n_nos_explorados += 1 

            if current_backward.getId() in self.m_graph.keys():
                for neighbor_bwd in self.get_predecessors(current_backward):
                    node_bwd = self.get_node_by_id(neighbor_bwd)
                    if node_bwd not in backward_visited and self.get_edge_by_nodes(node_bwd, current_backward) is not None and not self.get_edge_by_nodes(node_bwd, current_backward).isCortada():
                        edge_bwd = self.get_edge_by_nodes(node_bwd, current_backward)
                        if edge_bwd.isTransito():
                            lista_transito.append(edge_bwd)
                        backward_queue.put(node_bwd)
                        backward_parent[node_bwd] = current_backward
                        backward_visited.add(node_bwd)
                        n_nos_explorados += 1
        
        path = self.reconstruct_path_bidirectional(path_found, meeting_point, forward_parent, backward_parent)
        costT = self.calcula_custo(path, lista_transito)
        return (path, costT, n_nos_explorados)

    def get_predecessors(self, node):
        """
        Method to get the predecessors of a certin node, it is needed to make the backwards exploration in the bidirectional search
        :param node(Node Object): The current node that is going to be searched for adjacent ocurrences in the graph
        :raturn: A list of the predecessor's node's names
        """
        predecessors = []
        for (nodo, adj) in self.m_graph.items():
            for (neighbor, cost, k) in adj:
                if neighbor == node.getId():
                    predecessors.append(nodo)
        return predecessors


    def reconstruct_path_bidirectional(self, path_found, meet, forward_dic, backward_dic):
        """
        Method to reconstructs the final path of the bidirectional search "joining" both forward and backward paths
        :param meet(Node Object): The node where the forward and backward exploration meet
        :param forwar_dic(Dic{Object Node : Object Node}): The parent dictonary for the forward search used to find out the order of the nodes
        :param backward_dic(Dic{Object Node : Object Node}): The parent dictonary for the backward search used to find out the order of the nodes
        :return: A list of nodes representing the found path of the bidirectional search
        """
        start_path=[]
        end_path=[]
        final_path = []
        current = meet
        if path_found:
            start_path.append(current)
            while forward_dic[current] is not None:
                start_path.append(forward_dic[current])
                current = forward_dic[current]
            start_path.reverse()
            current = meet
            while backward_dic[current] is not None:
                end_path.append(backward_dic[current])
                current = backward_dic[current]
            #end_path.reverse()

            final_path = start_path + end_path
        return final_path
            

    #####################################
    #       Procura Custo Uniforme      #
    #####################################
        
    def procura_custo_uniforme(self, start, end):
        """
        Uniform Cost search adapted to our graph and circumstances using a min-heap to keep track of the lower cost possible moves
        :param start(Node Object): The start node object
        :param end(Node Object): The end node object
        :return: A list of nodes representing the path from the start node to the end node and the total cost pair
        """
        n_nos_explorados=0
        lista_transito=[]
        priority_queue = [(0, start)]
        visited = set()
        parents = dict()
        parents[start] = None
        path_found = False

        while priority_queue and not path_found:
            current_prio, current_node = heapq.heappop(priority_queue)

            if current_node == end:
                path_found = True

            if current_node  in visited:
                continue # Passa para a próxima iteração do loop
            
            visited.add(current_node) 

            if current_node.getId() in self.m_graph.keys():
                for (adj, cost, k) in self.m_graph[current_node.getId()]:
                    prox_nodo = self.get_node_by_id(adj)
                    if prox_nodo not in visited and not self.get_edge_by_nodes(current_node, prox_nodo).isCortada():
                        edge = self.get_edge_by_nodes(current_node, prox_nodo)
                        if edge.isTransito():
                            lista_transito.append(edge)
                        parents[prox_nodo] = current_node
                        heapq.heappush(priority_queue, (current_prio+cost, prox_nodo))
                        n_nos_explorados += 1

        path=[]
        custoT = []
        if path_found:
            path.append(end)
            while parents[end] is not None:
                path.append(parents[end])
                end = parents[end]
            path.reverse()
            custoT = self.calcula_custo(path, lista_transito)
        return (path, custoT, n_nos_explorados)
    
    ######################################
    #         Procura Iterativa          #
    #     Aprofundamento Progressivo     #
    ######################################

    def procura_iterativa(self, start, end):
        """
        Method responsible to iterate thought the searches, increasing the depth until a path is found
        :param start(Node Object): The start node object
        :param end(Node Object): The end node object
        :return: A list of nodes representing the path from the start node to the end node and the total cost pair
        """
        for limit in range(1, sys.maxsize):
            result = self.procura_iterativa_ciclo(start, end, limit, [], set(), [], 0)
            if result is not None:
                resultado, lista, n_nos = result
                custoT = self.calcula_custo(resultado, lista)
                return (resultado, custoT, n_nos)
       

    def procura_iterativa_ciclo(self, current, end, depth_limit, path, visited, lista_transito, n_nos_explorados):
        """
        The body of the Iterative Deepening search algorithm, basically a copy of the DFS algorithm with a few more verifications
        :param current(Node Object): The current node object of the recursive call
        :param end(Node Object): The end node object
        :param depth_limit: The number of recursions (depth) the method is "allowed" to perform at the moment
        :param path(List[Node Object]): The current path taken (used for recursion)
        :param visited(Set{Node Object}): A set to keep track of what nodes have been visited
        :param lista_transito(List[Ruas Object]): A list of edges that had traffic in them when the algorithms passed thought them
        :return: A list of nodes representing the path from the start node to the end node 
        """
        
        if current == end:
            path.append(current)
            visited.add(current)
            return (path, lista_transito, n_nos_explorados)

        if depth_limit == 0:
            return None

        path.append(current)
        visited.add(current)

        if current.getId() in self.m_graph.keys():
            for (adjacente, peso, k) in self.m_graph[current.getId()]:
                nodo = self.get_node_by_id(adjacente)
                if nodo not in visited and not self.get_edge_by_nodes(current, nodo).isCortada():
                    edge = self.get_edge_by_nodes(current, nodo)
                    if edge.isTransito():
                        lista_transito.append(edge)
                    resultado = self.procura_iterativa_ciclo(nodo, end, depth_limit - 1, path, visited, lista_transito, n_nos_explorados+1)
                    if resultado is not None:
                        return resultado

        path.pop()

        return None

        



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
    # ISTO VAI SER ALTERADO PARA MOSTRAR O MAPA REAL (VIDEO QUE ESTÁ NO #IDEIAS)
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

    def aestrela(self, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))  # o primeiro argumento do tuplo é o F(n)
        came_from = {}
        g_score = {node: float("inf") for node in self.m_graph}  # Distância menor para chegar do start ate este nodo
        g_score[start] = 0
        f_score = {node: float("inf") for node in self.m_graph}  # Distância predicted deste node até ao end node
        f_score[start] = self.m_h[start]
        close_list = set([])

        open_set_hash = {start}  # Set para ver o que está dentro da PriorityQueue

        while not open_set.empty():
            current = open_set.get()[2]  # Tirar da queue
            open_set_hash.remove(current)

            if current == end:
                path = self.reconstruct_path(came_from, current)
                path.reverse()
                return (path, self.calcula_custo(path))

            for (n, c) in self.getNeighbours(current):
                temp_g_score = g_score[current] + c

                if temp_g_score < g_score[n]:
                    came_from[n] = current
                    g_score[n] = temp_g_score
                    f_score[n] = temp_g_score + self.m_h[n]
                    if n not in open_set_hash:
                        count += 1
                        open_set.put((f_score[n], count, n))
                        open_set_hash.add(n)
                        # open_set.add(n)

            if current != start:
                close_list.add(current)

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
