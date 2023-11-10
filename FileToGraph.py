from Graph import Grafo
from Node import Node


class FileToGraph:

    def __init__(self, file_path):
        self.file_path = file_path

    def create_graph_from_file(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        graph = Grafo()

        for line in lines:
            # Encontrar a posição do primeiro espaço (separador entre id e nome)
            first_space_index = line.find(' ')

            # Extrair id e nome
            id, name_part = int(line[:first_space_index]), line[first_space_index + 1:]

            # Encontrar a posição do primeiro colchete (separador entre nome e lista de vizinhos)
            first_bracket_index = name_part.find('[')

            # Extrair o nome e a lista de vizinhos
            name, neighbors_str = name_part[:first_bracket_index].strip(), name_part[first_bracket_index:]

            # Extrair os vizinhos da lista de Tuplos
            neighbors = []
            for pair in neighbors_str[1:-1].split(')('):
                neighbor, cost = pair.split(',')
                neighbors.append((neighbor.strip(), int(''.join(c for c in cost if c.isdigit()))))

            # Adicionar o nodo e suas arestas ao grafo
            # Remover as aspas duplas do nome
            graph.add_edge(id, name.strip('"'), neighbors, neighbors[0][1])

        return graph


