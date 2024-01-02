from Graph import Grafo
from Node import Node
import Location



def main():
    print("-----Health Planet-----")
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
