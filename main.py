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
    

    """
    #start = grafoAtual.get_node_by_id(8321237017)
    #end = grafoAtual.get_node_by_id(2232799385)
    start = grafoAtual.get_node_by_id(8321237017)
    #end = grafoAtual.get_node_by_id(3103582239)
    end = grafoAtual.get_node_by_id(1675798722)
    path = grafoAtual.procura_DFS(start, end)
    print(path)
    print("\n")
    print(grafoAtual.converte_caminho(path[0]))"""
    print("---BSF---")
    start = grafoAtual.get_node_by_id(8321237017)
    #end = grafoAtual.get_node_by_id(1675798722)
    end = grafoAtual.get_node_by_id(1675798722)
    pathBFS = grafoAtual.procura_BFS(start, end)
    #path = grafoAtual.procura_DFS(start, end)
    #print(path)
    print(pathBFS)
    print("\n")
    print(grafoAtual.converte_caminho(pathBFS[0]))
    #print(grafoAtual.converte_caminho(path[0]))
    
    print("---Bidirecional---")
    pathBidirecional = grafoAtual.procura_bidirecional(start, end)
    print(pathBidirecional)
    print("\n")
    print(grafoAtual.converte_caminho(pathBidirecional[0]))
    
if __name__ == "__main__":
    main()
