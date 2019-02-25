import networkx as nx
import matplotlib.pyplot as plt
import LoadData
import numpy as np
from networkx import minimum_spanning_tree
from networkx import complete_graph

def visualizeData(data, distanceMatrix):
    G = nx.Graph()
    for i in range(len(data)):
        G.add_node(i)
    lst = []
    for i in range(len(distanceMatrix)):
        for j in range(i, len(distanceMatrix)):
            lst.append((i,j,distanceMatrix[i,j]))

    G.add_weighted_edges_from(lst)
    MST= minimum_spanning_tree(G)
    plt.subplot(121)
    nx.draw(MST, node_size=20, pos=data)
    #nx.draw(G, node_size=55, pos=data)
    print(MST.size(weight='weight'))
    plt.subplot(122)
    plt.scatter(data[:,0], data[:,1])
    plt.show()

