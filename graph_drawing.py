import json
from typing import List, Dict, Tuple, Any

import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from csv import reader


def load_nodes(path_nodes='graph_nodes.csv'):
    lista_nodi = list()
    with open('graph_nodes.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Check file as empty
        if header != None:
            # Iterate over each row after the header in the csv
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                lista_nodi.append(row[0:3])

    print("Numero nodi da rappresentare")
    print(len(lista_nodi))
    return lista_nodi


def load_edges(path_edges="graph.json"):
    graph = None
    with open(path_edges) as json_file:
        graph = json.load(json_file)

    lista_archi = list()
    for arco in graph["links"]:
        lista_archi.append((arco["source"], arco["target"]))

    print("Archi da rappresentare")
    print(len(lista_archi))
    return lista_archi


def load_edges_label(path_edges_label="graph.json"):
    graph = None
    with open("graph.json") as json_file:
        graph = json.load(json_file)

    edge_labels = dict()
    for edge in graph["links"]:
        edge_labels[edge["source"], edge["target"]] = edge['action_description']

    print("Label archi da rappresentare")
    print(len(edge_labels))
    return edge_labels


def load_nodes_label(path="graph.json"):
    graph = None
    with open(path) as json_file:
        graph = json.load(json_file)

    node_labels = list()
    for node in graph["nodes"]:
        node_labels.append(node['label'])

    print("Label nodi")
    print(len(node_labels))
    return node_labels


def load_genere(path="graph.json"):
    graph = None
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


def drawing_2D(nodi, node_labels, links, link_label):
    G = nx.DiGraph()

    for nodo in nodi:
        G.add_nodes_from(nodo)

    G.add_edges_from(links)

    print("Numero di archi nel grafo")
    print(G.number_of_edges())
    print("Numero di nodi nel grafo")
    print(G.number_of_nodes())

    pos = nx.spring_layout(G, seed=2)
    nx.draw_networkx_nodes(G, alpha=0.4, pos=pos, )
    nx.draw_networkx_edges(G, width=0.5, pos=pos)
    nx.draw_networkx_edge_labels(G, edge_labels=link_label, pos=pos)

    #nx.draw_networkx(G, pos=pos, arrows=True, arrowsize=12, with_labels=True, node_size=250, style='dashed')

    pos = nx.spiral_layout(G, dim=2, resolution=1)
    pos = nx.spring_layout(G, seed=6, pos=pos)
    pos = nx.spring_layout(G, seed=2, pos=pos)

    plt.figure(3, figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_size=1000, width=3)
    plt.show()




def drawing_3D(nodi, node_labels, links, link_label):
    G = nx.DiGraph()

    for nodo in nodi:
        G.add_nodes_from(nodo)

    G.add_edges_from(links)

    pos = nx.spring_layout(G, seed=2)
    nx.draw_networkx_nodes(G, alpha=0.4, pos=pos)
    nx.draw_networkx_edges(G, width=0.5, pos=pos)
    nx.draw_networkx_edge_labels(G, edge_labels=link_label, pos=pos)

    nx.draw_networkx(G, pos=pos, arrows=True, arrowsize=15, with_labels=True, node_size=250, style='dashed')

    # pos = nx.spring_layout(G, seed=6)
    # pos = nx.kamada_kawai_layout(G)
    pos = nx.spring_layout(G, seed=2)
    # pos = nx.random_layout(G)

    nx.draw(G, pos, with_labels=True)
    plt.show()


nodes = load_nodes()
node_label = load_nodes_label()

edges = load_edges()
links_label = load_edges_label()

drawing_2D(nodi=nodes, node_labels=node_label, links=edges, link_label=links_label)

load_genere()