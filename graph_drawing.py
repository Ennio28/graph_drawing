import json
import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from csv import reader
import json
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from csv import reader
import numpy as np
import random
import pandas as pd
import plotly.offline as py
import networkx as nx
import random
from mpl_toolkits.mplot3d import Axes3D



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
lista_nodi

def load_edges(path_edges="graph.json"):
    with open(path_edges) as json_file:
        graph = json.load(json_file)

    lista_archi = list()
    for arco in graph["links"]:
        lista_archi.append((arco["source"], arco["target"]))

    print("Archi da rappresentare")
    print(len(lista_archi))
    return lista_archi


lista_archi = load_edges()
lista_archi

Num_nodes = 43

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


with open('graph.json') as json_file:
    graph = json.load(json_file)

maschi = list()
femmine = list()
neutri = list()

for node in graph["nodes"]:
    if int(node["gender"]) == 0:
        neutri.append(node["id"])

    if int(node["gender"]) == 1:
        maschi.append(node["id"])

    if int(node["gender"]) == 2:
        femmine.append(node['gender'])

print(len(neutri) + len(maschi) + len(femmine))


G = nx.MultiDiGraph()

print("Numero nodi da rappresentare:")
print(len(lista_nodi))
print("-----------------------------")
print("Numero archi da rappresentare:")
print(len(lista_archi))



G.add_nodes_from(lista_nodi)
for nodo in lista_archi:
    G.add_edge(nodo[0], nodo[1], label= lista_label_archi.pop(0))


lista_label_archi = load_edges_label()
#G.add_weighted_edges_from(lista_archi)

print("Numero nodi nel grafo:")
print(G.number_of_nodes())
print("-----------------------")
print("Numero archi nel grafo:")
print(G.number_of_edges())

spiral = nx.spiral_layout(G, resolution=2.5)
spring_pos = nx.spring_layout(G, seed = 10,k = 0.5, pos = spiral)
kamada_pos = nx.kamada_kawai_layout(G, scale=1.2, pos = spring_pos)
spring_pos = nx.spring_layout(G, seed = 110, k = 3.5, pos = kamada_pos, scale=10, center=(0, 0))

plt.tight_layout()
plt.figure(3, figsize=(10, 10))

#Disegno nodi maschi
nx.draw(G, pos= spring_pos, with_labels=True,font_size=15,nodelist = maschi,node_color='#3776ab', node_size=600,alpha= 0.4,width= 0.4, labels= lista_label,arrowsize=10)

#Disegno nodi femmine
nx.draw(G, pos= spring_pos, with_labels=True,font_size=15,nodelist = femmine,node_color='#76ab37', node_size=600,alpha= 0.4,width= 0.4, labels= lista_label,arrowsize=10)

#Disegno nodi neutri
nx.draw(G, pos= spring_pos, with_labels=True,font_size=15,nodelist = neutri,node_color='#ab3776', node_size=600,alpha= 0.4,width= 0.4, labels= lista_label,arrowsize=10)
plt.show()
print("Numero nodi nel grafo:")
print(G.number_of_nodes())
print("-----------------------")
print("Numero archi nel grafo:")
print(G.number_of_edges())



plt.savefig('networkx_graph.png')
nx.drawing.nx_pydot.write_dot(G, 'multi.dot')

n = G.number_of_nodes()
pos = nx.spring_layout(G,dim=3, seed=18)


with plt.style.context(('ggplot')):
    fig = plt.figure(figsize=(10,10))
    ax = Axes3D(fig)

    for key, value in pos.items():
        xi = value[0]
        yi = value[1]
        zi = value[2]

        ax.scatter(xi,yi,zi, alpha =0.7)

    for i,j in enumerate(G.edges):
        x = np.array((pos[j[0]][0], pos[j[1]][0]))
        y = np.array((pos[j[0]][1], pos[j[1]][1]))
        z = np.array((pos[j[0]][2], pos[j[1]][2]))

        ax.plot(x,y,z,  alpha = 0.5)


    ax.view_init(30, 0)

    ax.set_axis_off()

    plt.show()

spring_3D = nx.spring_layout(G, dim=3, seed=1001)
# numpy array of x,y,z positions in sorted node order
xyz = np.array([spring_3D[v] for v in sorted(G)])

xyz


spring_3D = nx.spring_layout(G,dim=3, seed=18)



i = 1
while i <= Num_nodes:
    x_nodes = [spring_3D[str(i)][0]]# x-coordinates of nodes
    y_nodes = [spring_3D[str(i)][1]]# y-coordinates
    z_nodes = [spring_3D[str(i)][2]]# z-coordinates
    i = i +1

edge_list = G.edges()
edge_list

#we  need to create lists that contain the starting and ending coordinates of each edge.
x_edges=[]
y_edges=[]
z_edges=[]

#need to fill these with all of the coordiates
for edge in edge_list:
    #format: [beginning,ending,None]
    x_coords = [spring_3D[edge[0]][0],spring_3D[edge[1]][0],None]
    x_edges += x_coords

    y_coords = [spring_3D[edge[0]][1],spring_3D[edge[1]][1],None]
    y_edges += y_coords

    z_coords = [spring_3D[edge[0]][2],spring_3D[edge[1]][2],None]
    z_edges += z_coords


trace_edges = go.Scatter3d(x=x_edges,
                        y=y_edges,
                        z=z_edges,
                        mode='lines',
                        line=dict(color='black', width=2),
                        hoverinfo='none')


trace_nodes = go.Scatter3d(x=x_nodes,
                        y=y_nodes,
                        z=z_nodes,
                        mode='markers',
                        marker=dict(symbol='circle',
                                    size=10,
                                    colorscale=['lightgreen','magenta'], #either green or mageneta
                                    line=dict(color='black', width=0.5)),

                        hoverinfo='text')

axis = dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title='')

#also need to create the layout for our plot
layout = go.Layout(title="Two Predicted Factions of Zachary's Karate Club",
                width=650,
                height=625,
                showlegend=False,
                scene=dict(xaxis=dict(axis),
                        yaxis=dict(axis),
                        zaxis=dict(axis),
                        ),
                margin=dict(t=100),
                hovermode='closest')

#Include the traces we want to plot and create a figure
data = [trace_edges, trace_nodes]
fig = go.Figure(data=data, layout=layout)

fig.show()



