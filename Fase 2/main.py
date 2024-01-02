import os
from time import sleep
import re
import os
import cProfile
from prettytable import PrettyTable

from Graph import Grafo
from Node import Node
import Location
from HealthPlanet import HealthPlanet



def main():
    #print("-----Health Planet-----")

    health_planet = HealthPlanet()

    cliente_logado = None  # Variável para rastrear o usuário logado

    while True:
        if cliente_logado is None:
            print(
                "\n=========================================== Health Planet ===============================================")
            print("HealthPlanet.help> 'registo [username] [password]' - Registar um novo utilizador")
            print("HealthPlanet.help> 'login [username] [password]'    - Login de um Utilizador já existente")
            print(
                "=========================================================================================================")

            escolha = input("HealthPlanet.help> ")

            if escolha.startswith('registo'):
                # Processo de registro
                parametros = escolha.split(' ')
                if len(parametros) == 3:
                    nome_usuario = parametros[1]
                    senha = parametros[2]
                    health_planet.adicionar_cliente(nome_usuario, senha)
                else:
                    print("[SYS] Erro: Registo incorreto. Digite 'register [username] [password]'.")

            elif escolha.startswith('login'):
                # Processo de login
                parametros = escolha.split(' ')
                if len(parametros) == 3:
                    nome_usuario = parametros[1]
                    senha = parametros[2]
                    if nome_usuario in health_planet.users and health_planet.users[nome_usuario].password == senha:
                        cliente_logado = health_planet.users[nome_usuario]
                        print("[SYS] Login bem-sucedido!")
                    else:
                        print("[SYS] Erro: Nome de usuário ou senha incorretos.")
                else:
                    print("[SYS] Erro: Login incorreto. Digite 'login [username] [password]'.")

            else:
                print("[SYS] Erro: Comando inválido.")

        else:
            print(
                "\n=========================================== Health Planet ===============================================")
            print("HealthPlanet.menu> 'nova_encomenda'  - Criar uma nova encomenda")
            print("HealthPlanet.menu> 'ver_encomendas'             - Ver suas encomendas")
            print("HealthPlanet.menu> 'logout'                      - Logout e voltar ao menu principal")
            print(
                "=========================================================================================================")

            escolha = input("HealthPlanet.menu> ")

            if escolha == 'nova_encomenda':
                # Processo de criação de nova encomenda
                localizacao = input("[SYS] Selecione uma cidade (formato: Cidade, País): ")
                neigh, edges, nodes = Location.run(localizacao)
                grafoAtual = Grafo(nodes, neigh, edges)

                numero_produtos = int(input("[SYS] Digite o número de produtos: "))

                detalhes_produtos = []
                peso_total = 0
                for _ in range(numero_produtos):
                    nome_produto = input("[SYS] Digite o nome do produto: ")
                    peso_produto = float(input("[SYS]Digite o peso do produto: "))
                    peso_total += peso_produto
                    detalhes_produtos.append((nome_produto, peso_produto))
                    print("\n")

                urgencia_entrega = input("[SYS] Escolha a urgência de entrega (imediata/urgente/normal/irrelevante): ").lower()
                origem, destino = seleciona_origem_destino(grafoAtual)
                if urgencia_entrega not in ['imediata', 'urgente', 'normal', 'irrelevante']:
                    print("[SYS] Erro: Escolha de urgência inválida.")
                else:
                    health_planet.adicionar_encomenda(cliente_logado,peso_total,detalhes_produtos,origem,destino,urgencia_entrega)
                    print("[SYS] Encomenda criada com sucesso!")

            elif escolha == 'ver_encomendas':
                encomendas_cliente = health_planet.get_encomendas_cliente(cliente_logado)
                if encomendas_cliente:
                    print("[SYS] Encomendas do cliente:")
                    for encomenda in encomendas_cliente:
                        print(encomenda)
                else:
                    print("[SYS] O cliente ainda não possui encomendas.")

            elif escolha == 'logout':
                print("[SYS] Logout realizado com sucesso!")
                cliente_logado = None  # Volta ao estado de nenhum usuário logado

            else:
                print("[SYS] Erro: Comando inválido.")

    # location = input("Selecione uma cidade (formato: Cidade, País): ")  # Define the location (you can specify a city, coordinates, etc.)
    location = "Braga, Portugal" # Deixar assim para teste
    neigh, edges, nodes = Location.run(location)

    #print(edges)
    grafoAtual = Grafo(nodes, neigh, edges)
    # for edge in edges:
    #    if edge.getOrigem() == 263568202 or edge.getDestino() == 263568202:
    #        print(edge)
    #start, end = seleciona_origem_destino(grafoAtual)
    start = grafoAtual.get_node_by_id(8321237017)
    end = grafoAtual.get_node_by_id(1675798722)
    
    
    # for adj in neigh.values():
    #     seen_element=set()
    #     for (adjacente, custo, k) in adj:
    #         if adjacente in seen_element:
    #             print(adj)
    #         else: seen_element.add(adjacente)
    
    """
    print("---DFS---")
    pathDFS = grafoAtual.procura_DFS(start, end)
    print(pathDFS)
    print("\n")
    print(grafoAtual.converte_caminho(pathDFS[0]))
    
    print("---BSF---")
    pathBFS = grafoAtual.procura_BFS(start, end)
    print(pathBFS)
    print("\n")
    print(grafoAtual.converte_caminho(pathBFS[0]))
    
    print("---Bidirecional---")
    pathBidirecional = grafoAtual.procura_bidirecional(start, end)
    print(pathBidirecional)
    print("\n")
    print(grafoAtual.converte_caminho(pathBidirecional[0]))

    print("---Custo Uniforme---")
    pathCustoUniforme = grafoAtual.procura_custo_uniforme(start, end)
    print(pathCustoUniforme)
    print("\n")
    print(grafoAtual.converte_caminho(pathCustoUniforme[0]))

    print("---Procura Iterativa---")
    pathProcuraIterativa = grafoAtual.procura_iterativa(start, end)
    print(pathProcuraIterativa)
    print("\n")
    print(grafoAtual.converte_caminho(pathProcuraIterativa[0]))
    """

    print("---Procura AStar---")
    grafoAtual.calcula_heuristica_global(end)
    pathProcuraAStar = grafoAtual.procura_aStar(start, end, "car")
    print(pathProcuraAStar)
    print("\n")
    print(grafoAtual.converte_caminho(pathProcuraAStar[0]))

def seleciona_origem_destino(graph):
    testO1, testO2, testD1, testD2 = str(), str(), str(), str()

    print(
        "[SYS] Os pontos de origem e destino são nodos que são representados pela interseção de duas ou mais ruas")
    print("[SYS] O processo de seleção de origem e destino é o seguinte: ")
    print("[SYS] -> Indicar uma rua")
    print("[SYS] -> Indicar outra rua que faça interseção com a original")

    while isinstance(testO1, str):
        ruaOrigem1 = input("[SYS] Indique a rua de origem principal: ")
        testO1 = graph.get_edge_by_name(ruaOrigem1)
        print("\n")
        print(testO1)
        print("\n")

    while isinstance(testO2, str):
        ruaOrigem2 = input("[SYS] Indique a rua que faça interceção com a original de origem: ")
        testO2 = graph.get_edge_by_name(ruaOrigem2)
        print("\n")
        print(testO2)
        print("\n")

    intersectionOrigem = graph.get_intersection_node(testO1, testO2)

    while isinstance(testD1, str):
        ruaDestino1 = input("[SYS] Indique a rua de destino principal: ")
        testD1 = graph.get_edge_by_name(ruaDestino1)
        print("\n")
        print(testD1)
        print("\n")

    while isinstance(testD2, str):
        ruaDestino2 = input("[SYS] Indique a rua que faça interceção com a original de destino: ")
        testD2 = graph.get_edge_by_name(ruaDestino2)
        print("\n")
        print(testD2)
        print("\n")

    sleep(2)
    intersectionDetino = graph.get_intersection_node(testD1, testD2)
    os.system('cls')
    start = graph.get_node_by_id(intersectionOrigem)
    end = graph.get_node_by_id(intersectionDetino)
    return start, end




if __name__ == "__main__":
    main()
