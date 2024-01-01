from Graph import Grafo
from Node import Node
import Location
import cProfile



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

    performance_algoritmos(pathDFS[2], pathBFS[2], pathBidirecional[2], pathCustoUniforme[2], pathProcuraIterativa[2], profilerDFS, profilerBFS, profilerBidirecional, profilerCustoUniforme, profilerProcuraIterativa)

def seleciona_origem_destino(graph):
    testO1, testO2, testD1, testD2 = str(), str(), str(), str()
    
    print("[SYS] Os pontos de origem e destino são nodos que são representados pela interseção de duas ou mais ruas")
    print("[SYS] O processo de seleção de origem e destino é o seguinte: ")
    print("[SYS] -> Indicar uma rua")
    print("[SYS] -> Indicar outra rua que faça interseção com a original")

    while isinstance(testO1, str):
        ruaOrigem1 = input("[SYS] Indique a rua de origem principal: ")
        testO1 = graph.get_edge_by_name(ruaOrigem1)
        print(testO1)

    while isinstance(testO2, str):
        ruaOrigem2  = input("[SYS] Indique a rua que faça interceção com a original de origem: ")
        testO2 = graph.get_edge_by_name(ruaOrigem2)
        print(testO2)
    
    intersectionOrigem = graph.get_intersection_node(testO1, testO2)

    while isinstance(testD1, str):
        ruaDestino1 = input("[SYS] Indique a rua de destino principal: ")
        testD1 = graph.get_edge_by_name(ruaDestino1)
        print(testD1)

    while isinstance(testD2, str):
        ruaDestino2 = input("[SYS] Indique a rua que faça interceção com a original de destino: ")
        testD2 = graph.get_edge_by_name(ruaDestino2)
        print(testD2)

    intersectionDetino = graph.get_intersection_node(testD1, testD2)

    start = graph.get_node_by_id(intersectionOrigem)
    end = graph.get_node_by_id(intersectionDetino)
    return start, end

    

def performance_algoritmos(tempDFS, tempBFS, tempBidirecional, tempCustoUniforme, tempIterativa, profilerDFS, profilerBFS, profilerBidirecional, profilerCustoUniforme, profilerProcuraIterativa):
    print("CHEGIE A PERFORMANCE")

if __name__ == "__main__":
    main()
