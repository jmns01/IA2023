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
    location = "Braga, Portugal"  # Deixar assim para teste
    neigh, edges, nodes,a,b,c,d = Location.run(location)
    grafoAtual = Grafo(nodes, neigh, edges,a,b,c,d)

    # start, end = seleciona_origem_destino(grafoAtual)
    start = grafoAtual.get_node_by_id(8321237017)
    end = grafoAtual.get_node_by_id(1675798722)
    grafoAtual.calcula_heuristica_global(end)
    print("---Procura A*---")
    profilerAstar = cProfile.Profile()
    profilerAstar.enable()
    pathAstar = grafoAtual.procura_aStar(start, end,"car")
    profilerAstar.disable()
    if len(pathAstar[0]) > 0:
        print("\n[SYS] Caminho Encontrado: ")
        print(grafoAtual.converte_caminho(pathAstar[0]))
        print("\n[SYS] Custo: ")
        print(pathAstar[1])
        print("\n")
    else:
        print("\n[SYS] Caminho não encontrado!")

    performance_algoritmos(pathAstar,
                           [
                    profilerAstar])


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
                if not health_planet.check_if_graph_exists(localizacao):
                    neigh, edges, nodes, drive, drive_list, bike, bike_list = Location.run(localizacao)
                    grafoAtual = Grafo(nodes, neigh, edges, drive, drive_list, bike, bike_list)
                    health_planet.adicionar_grafo(localizacao,grafoAtual)

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

    print("---Procura AStar---")
    grafoAtual.calcula_heuristica_global(end)
    pathProcuraAStar = grafoAtual.procura_aStar(start, end, "car")
    print(pathProcuraAStar)
    print("\n")
    print(grafoAtual.converte_caminho(pathProcuraAStar[0]))

def seleciona_origem_destino(graph):
    testO1, testO2, testD1, testD2 = str(), str(), str(), str()

    print("[SYS] Os pontos de origem e destino são nodos que são representados pela interseção de duas ou mais ruas")
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


def performance_algoritmos(pathAstar,
                           profiles):
    table = PrettyTable()
    dicionario = dict()
    algoritmos = ['DFS', 'BFS', 'Bidirecional', 'Custo Uniforme', 'Procura Iterativa', 'A*']

    dicionario['Algoritmo'] = algoritmos
    dicionario['Tempo de Execução'] = []
    dicionario['Número de Chamadas de Funções'] = []
    dicionario['Tamanho do Path'] = []
    dicionario['Custo de Solução'] = []
    dicionario['Número de Nós Explorados'] = []

    for profile in profiles:
        stats = pstats.Stats(profile)
        tempo = stats.total_tt
        num_cals = stats.total_calls
        dicionario['Tempo de Execução'].append(tempo)
        dicionario['Número de Chamadas de Funções'].append(num_cals)

    dicionario['Tamanho do Path'].append(len(pathDFS[0]))
    dicionario['Tamanho do Path'].append(len(pathBFS[0]))
    dicionario['Tamanho do Path'].append(len(pathBidirecional[0]))
    dicionario['Tamanho do Path'].append(len(pathCustoUniforme[0]))
    dicionario['Tamanho do Path'].append(len(pathProcuraIterativa[0]))
    dicionario['Tamanho do Path'].append(len(pathAstar[0]))

    dicionario['Custo de Solução'].append(pathDFS[1])
    dicionario['Custo de Solução'].append(pathBFS[1])
    dicionario['Custo de Solução'].append(pathBidirecional[1])
    dicionario['Custo de Solução'].append(pathCustoUniforme[1])
    dicionario['Custo de Solução'].append(pathProcuraIterativa[1])
    dicionario['Custo de Solução'].append(pathAstar[1])

    dicionario['Número de Nós Explorados'].append(pathDFS[2])
    dicionario['Número de Nós Explorados'].append(pathBFS[2])
    dicionario['Número de Nós Explorados'].append(pathBidirecional[2])
    dicionario['Número de Nós Explorados'].append(pathCustoUniforme[2])
    dicionario['Número de Nós Explorados'].append(pathProcuraIterativa[2])
    dicionario['Número de Nós Explorados'].append(pathAstar[2])

    table.field_names = ['Algoritmo', 'Tempo de Execução', 'Número de Chamadas de Funções', 'Tamanho do Path',
                         'Custo de Solução', 'Número de Nós Explorados']
    for i in range(len(dicionario['Algoritmo'])):
        row = [
            dicionario['Algoritmo'][i],
            dicionario['Tempo de Execução'][i],
            dicionario['Número de Chamadas de Funções'][i],
            dicionario['Tamanho do Path'][i],
            dicionario['Custo de Solução'][i],
            dicionario['Número de Nós Explorados'][i]
        ]
        table.add_row(row)

    print(table)

    yes = r'(?i)\b(?:yes|y)\b'
    no = r'(?i)\b(?:no|n)\b'
    i = 0
    r = input("Quer ver informação com mais detalhe? (yes/no): ")
    if re.match(yes, r):
        for profile in profiles:
            print(f'---{algoritmos[i]}---')
            profile.print_stats(sort='cumulative')
            i += 1
    elif re.match(no, r):
        return

if __name__ == "__main__":
    main()
