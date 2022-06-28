import json
import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from csv import reader


def load_nodes(path_nodes='graph_nodes.csv'):
    lista_nodi = list()
    with open(path_nodes, 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Check file as empty
        if header is not None:
            # Iterate over each row after the header in the csv
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                lista_nodi.append(row[0:1])

    print("Numero nodi da rappresentare")
    print(len(lista_nodi))
    return lista_nodi


def load_edges(path_edges="graph_edges.csv"):
    lista_Archi = list()
    with open(path_edges, 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Check file as empty
        if header is not None:
            # Iterate over each row after the header in the csv
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                lista_Archi.append(row[0:3])

    print("Numero di archi da rappresentare:")
    print(len(lista_Archi))
    return lista_Archi


def load_edges_label(path_edges_label="graph.json"):
    lista_label_edges = list()
    with open(path_edges_label, 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Check file as empty
        if header is not None:
            # Iterate over each row after the header in the csv
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                lista_label_edges.append(row[0:3])

    return lista_label_edges


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

    label_archi = load_edges_label()

    G.add_edges_from(links)
    print("Numero di archi nel grafo")
    print(G.number_of_edges())
    print("Numero di nodi nel grafo")
    print(G.number_of_nodes())

    print("Calcolo della posizione con spring")
    pos = nx.spiral_layout(G, scale=2, resolution=10)
    pos = nx.spring_layout(G, seed=2, pos=pos)
    nx.draw_networkx_nodes(G, alpha=0.4, pos=pos, label=node_labels)
    nx.draw_networkx_edges(G, width=0.9, pos=pos, arrowsize=200)

    plt.figure(3, figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_size=450)
    plt.show()


def drawing_3D(nodi, node_labels, links):
    print("Inizio del disegno")
    G = nx.MultiDiGraph()

    for nodo in nodi:
        G.add_nodes_from(nodo)

    G.add_edges_from(links)

    print("Calcolo della posizione con spring")
    pos = nx.spring_layout(G, seed=2)
    nx.draw_networkx_nodes(G, alpha=0.4, pos=pos)
    nx.draw_networkx_edges(G, width=8, alpha=0.3, node_size=450, pos=pos, arrowsize=200)

    spring_3D = nx.spring_layout(G, dim=3, seed=18)

    Num_nodes = G.number_of_nodes()

    x_nodes = [spring_3D[i][0] for i in range(Num_nodes)]  # x-coordinates of nodes
    y_nodes = [spring_3D[i][1] for i in range(Num_nodes)]  # y-coordinates
    z_nodes = [spring_3D[i][2] for i in range(Num_nodes)]  # z-coordinates

    edge_list = G.edges()

    # we  need to create lists that contain the starting and ending coordinates of each edge.
    x_edges = []
    y_edges = []
    z_edges = []

    # need to fill these with all of the coordiates
    for edge in edge_list:
        # format: [beginning,ending,None]
        x_coords = [spring_3D[edge[0]][0], spring_3D[edge[1]][0], None]
        x_edges += x_coords

        y_coords = [spring_3D[edge[0]][1], spring_3D[edge[1]][1], None]
        y_edges += y_coords

        z_coords = [spring_3D[edge[0]][2], spring_3D[edge[1]][2], None]
        z_edges += z_coords

    # create a trace for the edges
    trace_edges = go.Scatter3d(x=x_edges,
                               y=y_edges,
                               z=z_edges,
                               mode='lines',
                               line=dict(color='black', width=2),
                               hoverinfo='none')

    # create a trace for the nodes
    trace_nodes = go.Scatter3d(x=x_nodes,
                               y=y_nodes,
                               z=z_nodes,
                               mode='markers',
                               marker=dict(symbol='circle',
                                           size=10,
                                           line=dict(color='black', width=0.5)),
                               text=node_labels,
                               hoverinfo='text')

    # we need to set the axis for the plot
    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title='')

    # also need to create the layout for our plot
    layout = go.Layout(title="Rappresentazione Saga",
                       width=650,
                       height=625,
                       showlegend=False,
                       scene=dict(xaxis=dict(axis),
                                  yaxis=dict(axis),
                                  zaxis=dict(axis),
                                  ),
                       margin=dict(t=100),
                       hovermode='closest')

    # Include the traces we want to plot and create a figure
    data = [trace_edges, trace_nodes]
    fig = go.Figure(data=data, layout=layout)

    fig.show()


nodes = load_nodes()
node_label = load_nodes_label()

edges = load_edges()
links_label = load_edges_label()

drawing_2D(nodi=nodes, node_labels=node_label, links=edges)
# drawing_3D(nodi=nodes, node_labels=node_label, links=edges)
# load_genere()
