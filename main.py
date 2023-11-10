from Graph import Grafo
from Node import Node


def main():
    # Criar instância de grafo
    g = Grafo()

    # Adicionar vertices ao grafo g

    g.add_edge2(1, "Rua A", [("Rua B", 100), ("Rua C", 200)], 50)
    g.add_edge2(2, "Rua B", [("Rua A", 50), ("Rua D", 75)], 100)
    g.add_edge2(3, "Rua C", [("Rua A", 50), ("Rua E", 125)], 200)
    g.add_edge2(4, "Rua D", [("Rua B", 100), ("Rua E", 125)], 75)
    g.add_edge2(5, "Rua E", [("Rua B", 100), ("Rua D", 75)], 125)

    r = g.dicBike("Rua A")
    print(r)

    
    

    '''
    saida = -1

    while saida != 0:
        print("1-Imprimir grafo ")
        print("2-Desenhar Grafo")
        print("3-Imprimir  nodos de Grafo")
        print("4-Imprimir arestas de Grafo")
        print("5-DFS")
        print("6-BFS")
        print("7 -Outra solução ")
        print("0-Saír")

        saida = int(input("introduza a sua opcao-> "))
        
        '''




if __name__ == "__main__":
    main()
