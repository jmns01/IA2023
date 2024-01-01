from Graph import Grafo
from Node import Node
import Location
import cProfile
from prettytable import PrettyTable
import pstats
import re
import os
from time import sleep


def main():
    print("-----------------------\n" +
          "-----Health Planet-----\n" +
          "-----------------------\n")
    #location = input("[SYS] Selecione uma cidade (formato: Cidade, País): ")  # Define the location (you can specify a city, coordinates, etc.)
    location = "Braga, Portugal" # Deixar assim para teste
    neigh, edges, nodes = Location.run(location)
    grafoAtual = Grafo(nodes, neigh, edges)
    
    start, end = seleciona_origem_destino(grafoAtual)
    print("--------------------\n" +
          "-----Algoritmos-----\n" +
          "--------------------\n")
    
    print("---DFS---")

    profilerDFS = cProfile.Profile()
    profilerDFS.enable()
    pathDFS = grafoAtual.procura_DFS(start, end)
    profilerDFS.disable()
    print("\n")
    print("[SYS] Caminho Encontrado: ")
    print(grafoAtual.converte_caminho(pathDFS[0]))
    print("[SYS] Custo: ")
    print(pathDFS[1])
    print("\n")
    
    print("---BSF---")

    profilerBFS = cProfile.Profile()
    profilerBFS.enable()
    pathBFS = grafoAtual.procura_BFS(start, end)
    profilerBFS.disable()
    print("\n")
    print("[SYS] Caminho Encontrado: ")
    print(grafoAtual.converte_caminho(pathBFS[0]))
    print("[SYS] Custo: ")
    print(pathBFS[1])
    print("\n")
    
    print("---Bidirecional---")

    profilerBidirecional = cProfile.Profile()
    profilerBidirecional.enable()
    pathBidirecional = grafoAtual.procura_bidirecional(start, end)
    profilerBidirecional.disable()
    print("\n")
    print("[SYS] Caminho Encontrado: ")
    print(grafoAtual.converte_caminho(pathBidirecional[0]))
    print("[SYS] Custo: ")
    print(pathBidirecional[1])
    print("\n")

    print("---Custo Uniforme---")

    profilerCustoUniforme = cProfile.Profile()
    profilerCustoUniforme.enable()
    pathCustoUniforme = grafoAtual.procura_custo_uniforme(start, end)
    profilerCustoUniforme.disable()
    print("\n")
    print("[SYS] Caminho Encontrado: ")
    print(grafoAtual.converte_caminho(pathCustoUniforme[0]))
    print("[SYS] Custo: ")
    print(pathCustoUniforme[1])
    print("\n")

    print("---Procura Iterativa---")
    profilerProcuraIterativa = cProfile.Profile()
    profilerProcuraIterativa.enable()
    pathProcuraIterativa = grafoAtual.procura_iterativa(start, end)
    profilerProcuraIterativa.disable()
    print("\n")
    print("[SYS] Caminho Encontrado: ")
    print(grafoAtual.converte_caminho(pathProcuraIterativa[0]))
    print("[SYS] Custo: ")
    print(pathProcuraIterativa[1])
    print("\n")

    performance_algoritmos(pathDFS, pathBFS, pathBidirecional, pathCustoUniforme, pathProcuraIterativa, [profilerDFS, profilerBFS, profilerBidirecional, profilerCustoUniforme, profilerProcuraIterativa])

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
        ruaOrigem2  = input("[SYS] Indique a rua que faça interceção com a original de origem: ")
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

    

def performance_algoritmos(pathDFS, pathBFS, pathBidirecional, pathCustoUniforme, pathProcuraIterativa, profiles):
    table = PrettyTable()
    dicionario = dict()
    algoritmos = ['DFS', 'BFS', 'Bidirecional', 'Custo Uniforme', 'Procura Iterativa']
    
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

    dicionario['Custo de Solução'].append(pathDFS[1])
    dicionario['Custo de Solução'].append(pathBFS[1])
    dicionario['Custo de Solução'].append(pathBidirecional[1])
    dicionario['Custo de Solução'].append(pathCustoUniforme[1])
    dicionario['Custo de Solução'].append(pathProcuraIterativa[1])

    dicionario['Número de Nós Explorados'].append(pathDFS[2])
    dicionario['Número de Nós Explorados'].append(pathBFS[2])
    dicionario['Número de Nós Explorados'].append(pathBidirecional[2])
    dicionario['Número de Nós Explorados'].append(pathCustoUniforme[2])
    dicionario['Número de Nós Explorados'].append(pathProcuraIterativa[2])
    
    table.field_names = ['Algoritmo', 'Tempo de Execução', 'Número de Chamadas de Funções', 'Tamanho do Path', 'Custo de Solução', 'Número de Nós Explorados']
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
    i=0
    r = input("Quer ver informação com mais detalhe? (yes/no): ")
    if re.match(yes, r):
        for profile in profiles:
            print(f'---{algoritmos[i]}---')
            profile.print_stats(sort='cumulative')
            i += 1
    elif re.match(no, r): return


if __name__ == "__main__":
    main()
