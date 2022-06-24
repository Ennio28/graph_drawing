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
    return lista_nodi


def load_edges(path_edges="graph.json"):
    graph = None
    with open(path_edges) as json_file:
        graph = json.load(json_file)

    lista_archi = list()
    for archi in graph["links"]:
        lista_archi.append((archi["source"], archi["target"]))

    return lista_archi


def load_edges_label(path_edges_label="graph.json"):
    graph = None
    with open("graph.json") as json_file:
        graph = json.load(json_file)

    edge_labels = dict()
    for edge in graph["links"]:
        edge_labels[(edge['source'], edge['target'])] = edge['action_description']

    return edge_labels


def load_nodes_label(path="graph.json"):
    graph = None
    with open("graph.json") as json_file:
        graph = json.load(json_file)

    node_labels = dict()
    for node in graph["nodes"]:
        node_labels[node['id']] = node['label']

    graph = None
    with open(path) as json_file:
        graph = json.load(json_file)

    node_labels = list()
    for node in graph["nodes"]:
        node_labels.append(node['label'])

    return node_labels


def drawing_2D(nodi, node_labels, links, link_label):
    G = nx.DiGraph()

    for nodo in nodi:
        G.add_nodes_from(nodo)

    G.add_edges_from(links)

    pos = nx.spring_layout(G, seed=2)
    pos = nx.kamada_kawai_layout(G, pos=pos)
    pos = nx.spring_layout(G, seed=2, pos=pos)

    nx.draw_networkx_nodes(G, pos=pos, alpha=0.4)
    nx.draw_networkx_edges(G, pos=pos, width=0.5)

    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=link_label)

   # nx.draw_networkx(G, pos=pos, arrows=True, arrowsize=15, with_labels=True, node_size=250, style='dashed')
    nx.draw(G, pos, with_labels=True)
    plt.show()


nodes = load_nodes()
print(len(nodes))
node_label = load_nodes_label()

edges = load_edges()
links_label = load_edges_label()

drawing_2D(nodi=nodes, node_labels=node_label, links=edges, link_label=links_label)
