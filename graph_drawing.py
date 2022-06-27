import json
import networkx as nx
#import plotly.graph_objects as go
import matplotlib.pyplot as plt
from csv import reader


def load_nodes(path_nodes='graph_nodes.csv'):
    lista_nodi = list()
    with open('graph_nodes.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Check file as empty
        if header is not None:
            # Iterate over each row after the header in the csv
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                lista_nodi.append(row[0:3])

    print("Numero nodi da rappresentare")
    print(len(lista_nodi))
    return lista_nodi


def load_edges(path_edges="graph.json"):
    with open(path_edges) as json_file:
        graph = json.load(json_file)

    lista_archi = list()
    for arco in graph["links"]:
        lista_archi.append((arco["source"], arco["target"]))

    print("Archi da rappresentare")
    print(len(lista_archi))
    return lista_archi


def load_edges_label(path_edges_label="graph.json"):
    with open(path_edges_label) as json_file:
        graph = json.load(json_file)

    edge_labels = dict()
    i = 1
    for edge in graph["links"]:
        edge_labels[(edge["source"], edge["target"], int(edge['action']) * i * 3)] = edge["action_description"]
        i = i + 1
    return edge_labels


def load_nodes_label(path="graph.json"):
    with open(path) as json_file:
        graph = json.load(json_file)

    node_labels = list()
    for node in graph["nodes"]:
        node_labels.append(node['label'])

    print("Label nodi")
    print(len(node_labels))
    return node_labels


def load_genere(path="graph.json"):
    with open(path) as json_file:
        graph = json.load(json_file)
    maschi = list()
    femmine = list()
    neutri = list()

    for node in graph["nodes"]:
        if int(node["gender"]) == 0:
            neutri.append(int(node["id"]))

        if int(node["gender"]) == 1:
            maschi.append(int(node["id"]))

        if int(node["gender"]) == 2:
            femmine.append(node['gender'])

    print(len(neutri) + len(maschi) + len(femmine))
    return neutri, maschi, femmine


def drawing_2D(nodi, node_labels, links):
    print("Inizio del disegno")
    G = nx.MultiDiGraph()

    for nodo in nodi:
        G.add_nodes_from(nodo)

    G.add_edges_from(links)



    print("Numero di archi nel grafo")
    print(G.number_of_edges())
    print("Numero di nodi nel grafo")
    print(G.number_of_nodes())

    with open("graph.json") as json_file:
        graph = json.load(json_file)

    edge_labels = list()
    for edge in graph["links"]:
        edge_labels.append((edge["source"], edge["target"], int(edge['action'])))
        G.add_weighted_edges_from(edge_labels[-1])

    print("Calcolo della posizione con spring")
    pos = nx.spring_layout(G, seed=2)
    nx.draw_networkx_nodes(G, alpha=0.4, pos=pos)
    nx.draw_networkx_edges(G, width=0.9, pos=pos, arrowsize=200)

    plt.figure(3, figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_size=450)
    plt.show()


nodes = load_nodes()
node_label = load_nodes_label()

edges = load_edges()
links_label = load_edges_label()

drawing_2D(nodi=nodes, node_labels=node_label, links=edges)

load_genere()
