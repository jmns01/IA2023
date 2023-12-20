from Graph import Grafo
from Node import Node
import Location



def main():
    print("-----Health Planet-----")
    # location = input("Selecione uma cidade (formato: Cidade, País): ")  # Define the location (you can specify a city, coordinates, etc.)
    location = "Braga, Portugal" # Deixar assim para teste
    neigh, edges, nodes = Location.run(location)

    #print(edges)
    grafoAtual = Grafo(False, nodes, neigh, edges)
    #for edge in edges:
    #    if edge.getOrigem() == 263568202 or edge.getDestino() == 263568202:
    #        print(edge)
    

    
    #start = grafoAtual.get_node_by_id(8321237017)
    #end = grafoAtual.get_node_by_id(2232799385)
    start = grafoAtual.get_node_by_id(8321237017)
    #end = grafoAtual.get_node_by_id(3103582239)
    end = grafoAtual.get_node_by_id(1675798722)
    path = grafoAtual.procura_DFS2(start, end)
    print(path)
    print("\n")
    print(grafoAtual.converte_caminho(path[0]))
    
if __name__ == "__main__":
    main()
