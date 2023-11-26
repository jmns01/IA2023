import sys
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import os
import pandas as pd



def create_neighborhood_dict(graph):
    neighborhood_dict = {}

    for u, v, k, data in graph.edges(keys=True, data=True):

        if u not in neighborhood_dict.keys():
            neighborhood_dict[u] = [(v,k)]
        else:
            neighborhood_dict[u].append((v,k))

        if not data.get('oneway', True):
            if v not in neighborhood_dict:
                neighborhood_dict[v] = [(u, k)]
            elif (u, k) not in neighborhood_dict[v]:  # Check if the reverse edge is already added
                neighborhood_dict[v].append((u, k))

    return neighborhood_dict

def create_edges_dict(graph):
    edges_dict = {}

    for u, v, k, data in graph.edges(keys=True, data=True):

        if (u,v,k) not in edges_dict.keys():
            edges_dict[(u,v,k)] = [data]


    return edges_dict

def create_nodes_dict(graph):
    node_dict = {}

    for node, data in G_filtered.nodes(data=True):

        if node not in node_dict.keys():
            node_dict[node] = [data]


    return node_dict


def get_node_by_number(self, number):
    for node, data in self.nodes(data=True):
        if node == number:
            print(f"Node {number} attributes: {data}")
            return node
    return None


def add_edge(self, node1, node2, length, name, oneway=False):
    super().add_edge(node1, node2, length=length, name=name, oneway=oneway)

    if node2 not in self.neighborhood_dict.get(node1, []):
        self.neighborhood_dict[node1].append(node2)

    if not oneway and node1 not in self.neighborhood_dict.get(node2, []):
        self.neighborhood_dict[node2].append(node1)


def get_arc_cost(graph, node1, node2):
    custoT = 0
    for u, v, k, data in graph.edges(keys=True, data=True):
        if u == node1 and v == node2:
            custoT += data.get('length')
    return custoT


def calcula_custo(graph, caminho):
    custo = 0
    i = 0
    while i + 1 < len(caminho):
        u, v = caminho[i], caminho[i + 1]
        custo += get_arc_cost(graph,u,v)
        i += 1
    return custo



def procura_DFS_AUX(graph, start, end, neighborhood_dict, path=[], visited=set()):
    path.append(start)
    visited.add(start)

    if start == end:
        custoT = calcula_custo(graph, path)
        return (path, custoT)
    for adjacente in list(neighborhood_dict[start]):  # Convert set to list
        if adjacente not in visited:
            resultado = procura_DFS_AUX(graph, adjacente, end, neighborhood_dict, path, visited)
            if resultado is not None:
                return resultado
    path.pop()
    return None

def procura_DFS(graph,path):
    i = 0
    dict=[]
    caminho = path[0]
    tamanho = path[1]
    while i + 1 < len(caminho):
        y, x = caminho[i], caminho[i+1]
        for u, v, k, data in graph.edges(keys=True, data=True):
            if u == y and v == x:
                dict.append(data.get('name'))
        i += 1
    print(dict,tamanho)



def get_nodes(self):
    for node, data in self.nodes(data=True):
        print(f"Node {node} attributes: {data}")


def get_neighborhood_dict(self):
    return self.neighborhood_dict



# Define the location (you can specify a city, coordinates, etc.)
location = "Braga, Portugal"

# Download the street network
G = ox.graph_from_place(location, network_type="drive")

# Convert the graph to a Pandas DataFrame
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

# Save the DataFrame to a CSV file
#edges.to_csv("street_network.csv", index=False)

#print(G.edges)




# Filter edges with a valid 'name' key
G_filtered = G.copy()



#G_filtered.remove_edges_from([(u, v) for u, v, data in G.edges(data=True) if 'name' not in data or data['name'] is None])

# # Keep only 'name' and 'length' keys in each node
# node_attributes = {node: {'name': data.get('name', None), 'length': data.get('length', None)} for node, data in G_filtered.nodes(data=True)}
# nx.set_node_attributes(G_filtered, node_attributes)
#
# edge_attributes = {(u, v, k): {'name': data.get('name', None), 'length': data.get('length', None)} for u, v, k, data in G_filtered.edges(keys=True, data=True)}
# nx.set_edge_attributes(G_filtered, edge_attributes)

for node, data in G_filtered.nodes(data=True):
    data.pop('name', None)
    data.pop('length', None)
    data.pop('highway', None)
    data.pop('ref', None)

for u, v, k, data in G_filtered.edges(keys=True, data=True):
    if data.get('junction') != 'roundabout' and data.get('name') is None:
        data.pop('osmid', None)
        data.pop('reversed', None)
        data.pop('geometry', None)
        data.pop('ref', None)
        data.pop('lanes', None)
    else:
        data.pop('highway', None)
        data.pop('osmid', None)
        data.pop('reversed', None)
        data.pop('geometry', None)
        data.pop('ref', None)
        data.pop('lanes', None)


name_counter = {}
for u, v, k, data in G_filtered.edges(keys=True, data=True):
    name = data.get('name')
    if name is not None:
        name_key = str(name)
        if name_key in name_counter:
            name_counter[name_key] += 1
            data['name'] = f"{name} ({name_counter[name_key]})"
        else:
            name_counter[name_key] = 1



# for u, v, data in G_filtered.edges(data=True):
#    print(f"Edge from {u} to {v} attributes:")
#    print(f"  Name: {data.get('name', None)}")
#    print(f"  Length: {data.get('length', None)}")
#    print("\n")



# # Iterate through the edges of the filtered graph
# for u, v, data in G_filtered.edges(data=True):
#     # Get the names of the nodes connected by the edge
#     node_u_name = data.get('name')
#     node_v_name = G_filtered.nodes[v].get('name')
#
#     # Handle the case where the names are lists by converting them to tuples
#     if isinstance(node_u_name, list):
#         node_u_name = tuple(node_u_name)
#     if isinstance(node_v_name, list):
#         node_v_name = tuple(node_v_name)
#
#     # Add node_v_name to the neighborhood of node_u_name
#     if node_u_name is not None:
#         if node_u_name not in neighborhood_dict:
#             neighborhood_dict[node_u_name] = [node_v_name]
#         else:
#             neighborhood_dict[node_u_name].append(node_v_name)
#
#     # Add node_u_name to the neighborhood of node_v_name
#     if node_v_name is not None:
#         if node_v_name not in neighborhood_dict:
#             neighborhood_dict[node_v_name] = [node_u_name]
#         else:
#             neighborhood_dict[node_v_name].append(node_u_name)

# Print the neighborhood dictionary
#for node_name, neighbors in neighborhood_dict.items():
#   print(f"Neighborhood of {node_name}: {neighbors}")
count =0
#
# for u, v, k, data in G_filtered.edges(keys=True, data=True):
# #      #if count == 1000:
# #          #break
# #      print(f"Edge ({u}, {v}, {k}) attributes: {data}")
# #      sys.stdout.flush()
# #      count = count + 1

#print(G_filtered.edges)


# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# print(G_filtered.edges)


# Initialize an empty dictionary to store the neighborhood of each node
# neighborhood_dict = {}
#
# # Iterate through the edges of the filtered graph
# for u, v, data in G_filtered.edges(data=True):
#     # Add v to the neighborhood of u
#     if u not in neighborhood_dict:
#         neighborhood_dict[u] = [v]
#     else:
#         neighborhood_dict[u].append(v)


#Print the neighborhood dictionary
#for node, neighbors in neighborhood_dict.items():
#    print(f"Neighborhood of {node}: {neighbors}")

# # Plot the street network
# fig, ax = ox.plot_graph(G_filtered, show=False, close=False, figsize=(10, 10))  10769646771   10816701879
# #
# #Show the plot
# plt.show()


# # # Get node positions
# node_positions = {node: (data['x'], data['y']) for node, data in G_filtered.nodes(data=True)}
#
# # Plot nodes
# nx.draw_networkx_nodes(G_filtered, pos=node_positions, node_size=2)
# #
# # # Plot edges
# nx.draw_networkx_edges(G_filtered, pos=node_positions, width=1)
# #
# plt.show()


# Assuming G_filtered is an instance of the NetworkX Graph class


# Now you can use the new method
#node_number = 11271544708  # Replace with the actual node number you're looking for
#node = G_filtered.get_node_by_number(node_number)
#G_filtered = CustomGraph(G_filtered)
# Obtenha o dicionário de vizinhos da instância
neighb = create_neighborhood_dict(G_filtered)
edges = create_edges_dict(G_filtered)
nodes = create_nodes_dict(G_filtered)
count=0
# for u, v, k, data in G_filtered.edges(keys=True, data=True):
#     count = count + 1
#     print(f"Edge ({u}, {v}, {k}) attributes: {data}")
#
# print(count)
#for node, data in G_filtered.nodes(data=True):
#     print(f"Node {node} attributes: {data}")

#Imprima o dicionário de vizinhos
# for node, neighbors in neighborhood_dict.items():
#     print(f"Neighborhood of {node}: {neighbors}")

#print(neighborhood_dict)
print(neighb)

#print(nodes)
# print(procura_DFS(G_filtered,11313827726, 11313807063,neighborhood_dict))

# for (u, v, k), data_list in edges.items():
#     if k != 0:
#         for data in data_list:
#             print(f"Edge ({u}, {v}, {k}) attributes: {data}")


# path = procura_DFS_AUX(G_filtered,11313827726, 11313807063,neighborhood_dict)

# path = procura_DFS_AUX(G_filtered,4053448599, 1461361056,neighborhood_dict)
# print(path)
# procura_DFS(G_filtered,path)
# for u, v, k, data in G_filtered.edges(keys=True, data=True):
#     if u == 11081088766 and v == 11081088771:
#         print(f"Edge ({u}, {v}, {k}) attributes: {data}")
#print(G_filtered.edges)
if G_filtered.has_edge(4053448594, 1461360979):
    print("True")

# edge_data_dict = G_filtered.get_edge_data(1898125189, 11313827673)
# key, edge_data = edge_data_dict.popitem()
# print(edge_data.get('length', 0))
#(4053448594, 4065304430):
#11081088766: [(11081088771, 0), (11081088771, 0)]
for u, v, k, data in G_filtered.edges(keys=True, data=True):
    if u==1898125189 and v==11313827673:
        print(f"{data}")


