import json
from csv import reader

import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go
import plotly.offline as py


def load_nodes(path_nodes='graph_nodes.csv'):
    lista_nodi = dict()
    with open(path_nodes, 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Check file as empty
        if header is not None:
            # Iterate over each row after the header in the csv
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                lista_nodi[row[0]] = row[1]

    print("Numero nodi da rappresentare")
    print(len(lista_nodi))
    return lista_nodi


lista_nodi = load_nodes()


def load_edges(path_edges="graph.json", interactive=False):
    with open(path_edges) as json_file:
        graph = json.load(json_file)

    lista_archi = list()

    if not interactive:
        for arco in graph["links"]:
            lista_archi.append((arco["source"], arco["target"]))

    if interactive:
        print('Interactive')
        for arco in graph["links"]:
            exit_count = lista_archi.count((arco["source"], arco["target"], arco['action']))
            if exit_count < 1:
                lista_archi.append((arco["source"], arco["target"], arco['action']))

    print("Archi da rappresentare")
    print(len(lista_archi))
    return lista_archi


lista_archi = load_edges(interactive=True)
lista_archi


def load_nodes_label(path_nodes="graph.json"):
    graph = None
    with open(path_nodes) as json_file:
        graph = json.load(json_file)

    node_labels = dict()
    for node in graph["nodes"]:
        node_labels[(node['id'])] = node['label']

    print("Numero di label dei nodi da rappresentare")
    print(len(node_labels))

    return node_labels


lista_label = load_nodes_label()

lista_label


def load_edges_label(path_edges="graph.json"):
    with open(path_edges) as json_file:
        graph = json.load(json_file)

    lista_label_archi = list()
    for arco in graph["links"]:
        lista_label_archi.append(arco["action_description"])

    print("Label archi da rappresentare")
    print(len(lista_archi))
    return lista_label_archi


lista_label_archi = load_edges_label()
print(len(lista_label_archi))
lista_label_archi


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


with open('graph.json') as json_file:
    graph = json.load(json_file)

maschi = list()
dizionario_maschi = dict()
femmine = list()
dizionario_femmine = dict()
neutri = list()
dizionario_neutri = dict()
lista_colori = list()

for node in graph["nodes"]:
    if int(node["gender"]) == 0:
        neutri.append(node["id"])
        dizionario_neutri[node["id"]] = node["label"]
        lista_colori.append('#ab3776')

    if int(node["gender"]) == 1:
        maschi.append(node["id"])
        dizionario_maschi[node["id"]] = node["label"]
        lista_colori.append('#3776ab')

    if int(node["gender"]) == 2:
        femmine.append(node['gender'])
        dizionario_femmine[node["id"]] = node["label"]
        lista_colori.append('#76ab37')

print(len(neutri) + len(maschi) + len(femmine))


def drawing_2D():
    G = nx.MultiDiGraph()
    lista_nodi = load_nodes()
    print("Numero nodi da rappresentare:")
    print(len(lista_nodi))
    print("-----------------------------")
    lista_archi = load_edges(interactive=False)
    print("Numero archi da rappresentare:")
    print(len(lista_archi))
    lista_label_archi = load_edges_label()

    G.add_nodes_from(lista_nodi)
    for nodo in lista_archi:
        G.add_edge(nodo[0], nodo[1], label=lista_label_archi.pop(0))

    lista_label_archi = load_edges_label()

    print("Numero nodi nel grafo:")
    print(G.number_of_nodes())
    print("-----------------------")
    print("Numero archi nel grafo:")
    print(G.number_of_edges())

    spiral = nx.spiral_layout(G, resolution=2.5)
    spring_pos = nx.spring_layout(G, seed=10, k=0.5, pos=spiral)
    kamada_pos = nx.kamada_kawai_layout(G, scale=1.2, pos=spring_pos)
    spring_pos = nx.spring_layout(G, seed=110, k=3.5, pos=kamada_pos, scale=10, center=(0, 0))

    plt.tight_layout()
    plt.figure(3, figsize=(10, 10))

    # Disegno nodi maschi
    nx.draw(G, pos=spring_pos, with_labels=True, font_size=15, nodelist=maschi, node_color='#3776ab', node_size=600,
            alpha=0.4, width=0.4, labels=lista_label, arrowsize=10)

    # Disegno nodi femmine
    nx.draw(G, pos=spring_pos, with_labels=True, font_size=15, nodelist=femmine, node_color='#76ab37', node_size=600,
            alpha=0.4, width=0.4, labels=lista_label, arrowsize=10)

    # Disegno nodi neutri
    nx.draw(G, pos=spring_pos, with_labels=True, font_size=15, nodelist=neutri, node_color='#ab3776', node_size=600,
            alpha=0.4, width=0.4, labels=lista_label, arrowsize=10)

    plt.figure(3, figsize=(10, 10))
    plt.show()
    print("Numero nodi nel grafo:")
    print(G.number_of_nodes())
    print("-----------------------")
    print("Numero archi nel grafo:")
    print(G.number_of_edges())


# drawing_2D()

def load_edge_label_interactive():
    with open('graph.json') as json_file:
        graph = json.load(json_file)

    lista_label = list()

    for arco in graph["links"]:
        exit_count = lista_label.count((arco["source"], arco["target"], arco['action_description']))
        if exit_count < 1:
            lista_label.append((arco["source"], arco["target"], arco['action_description']))

    print('Label archi interactive')
    print(len(lista_label))
    return lista_label


def drawing_2D_interactive():
    G = nx.MultiDiGraph()
    print("START DRAWING")
    lista_nodi = load_nodes()
    print(len(lista_nodi))
    print("-----------------------------")
    print("Numero archi da rappresentare:")
    lista_archi = load_edges(interactive=True)
    print(len(lista_archi))
    lista_label_archi = load_edge_label_interactive()

    G.add_nodes_from(lista_nodi)
    for arco in lista_archi:
        G.add_edge(arco[0], arco[1], label=lista_label_archi.pop(0))

    graph = None
    with open("graph.json") as json_file:
        graph = json.load(json_file)

        node_labels = list()
        for node in graph["nodes"]:
            node_labels.append(node['label'])

    print('Numero nodi nel grafo')
    print(G.number_of_nodes())
    print('Numero archi nel grafo')
    print(G.number_of_edges())

    spiral = nx.spiral_layout(G, resolution=2.5)
    spring_pos = nx.spring_layout(G, seed=10, k=1.5, pos=spiral)
    kamada_pos = nx.kamada_kawai_layout(G, scale=1.2, pos=spring_pos)
    spring_pos = nx.spring_layout(G, seed=110, k=1.5, pos=kamada_pos, scale=10, center=(0, 0))

    # we need to seperate the X,Y,Z coordinates for Plotly
    x_nodes_2D = [spring_pos[str(i)][0] for i in range(1, 43)]  # x-coordinates of nodes
    y_nodes_2D = [spring_pos[str(i)][1] for i in range(1, 43)]  # y-coordinates

    edge_list_2D = G.edges()

    # we  need to create lists that contain the starting and ending coordinates of each edge.
    x_edges_2D = []
    y_edges_2D = []

    x_text = []
    y_text = []

    # need to fill these with all of the coordiates
    for edge in edge_list_2D:
        # format: [beginning,ending,None]
        x_coords = [spring_pos[edge[0]][0], spring_pos[edge[1]][0], None]
        x_edges_2D += x_coords
        x_text.append((spring_pos[edge[0]][0] + spring_pos[edge[1]][0]) / 2)

        y_coords = [spring_pos[edge[0]][1], spring_pos[edge[1]][1], None]
        y_edges_2D += y_coords
        y_text.append((spring_pos[edge[0]][1] + spring_pos[edge[1]][1]) / 2)

    edge_label_trace = go.Scatter(x=x_text, y=y_text,
                                  mode='text',
                                  hoverinfo='text',
                                  text=lista_label_archi,
                                  textposition='middle center')

    trace_edges_2D = go.Scatter(x=x_edges_2D,
                                y=y_edges_2D,
                                mode='lines+text',
                                opacity=0.3,
                                line=dict(color='black', width=0.2),

                                marker=dict(size=8,
                                            opacity=0.3,
                                            line=dict(color='black', width=0.1)),
                                text=lista_label_archi,
                                hoverinfo='text')

    trace_nodes_2D = go.Scatter(x=x_nodes_2D,
                                y=y_nodes_2D,
                                mode='markers+text',
                                opacity=1,
                                # line=dict(color='white', width=0.5),
                                marker=dict(symbol='circle',
                                            size=18,
                                            opacity=0.5,
                                            color=lista_colori,
                                            line=dict(color='white', width=0.2)),
                                text=node_labels,
                                hoverinfo='text')

    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title='')

    edge_list_2D = G.edges()
    annotations = list()
    for edge in edge_list_2D:
        annotations.append(dict(ax=spring_pos[edge[0]][0], ay=spring_pos[edge[0]][1], axref='x', ayref='y',
                                x=spring_pos[edge[1]][0], y=spring_pos[edge[1]][1], xref='x', yref='y',
                                showarrow=True, arrowhead=5, arrowsize=1.3, ))

    # also need to create the layout for our plot
    layout = go.Layout(title="Rappresentazione interattiva della saga Hrafnkel",
                       width=1080,
                       height=1025,
                       showlegend=False,
                       annotations=annotations,
                       titlefont_size=16,
                       scene=dict(xaxis=dict(axis),
                                  yaxis=dict(axis),
                                  zaxis=dict(axis),
                                  ),
                       margin=dict(t=100),
                       hovermode='closest')

    # Include the traces we want to plot and create a figure
    data = [trace_edges_2D, trace_nodes_2D, edge_label_trace]
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), plot_bgcolor='rgb(255,255,255)')
    fig.update_layout(uniformtext_minsize=3)
    fig.show()
    py.plot(fig)


drawing_2D_interactive()
