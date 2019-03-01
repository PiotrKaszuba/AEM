import networkx as nx
import matplotlib.pyplot as plt


def visualizeData(nodes, distanceMatrix, data, edges=None):
    G = nx.Graph()
    for d in nodes:
        G.add_node(d)
    if edges is None:
        edges = []
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                edges.append((nodes[i],nodes[j],distanceMatrix[nodes[i],nodes[j]]))

    G.add_weighted_edges_from(edges)
    #MST= minimum_spanning_tree(G)
    plt.subplot(121)
    nx.draw(G, node_size=20, pos=data)
    #nx.draw(G, node_size=55, pos=data)
    #print(MST.size(weight='weight'))
    plt.subplot(122)
    plt.scatter(data[nodes,0], data[nodes,1])
    for edge in edges:
        edge = list(edge)
        pos = data[edge[:2]][:,0]
        plt.plot(data[edge[:2]][:,0], data[edge[:2]][:,1])
    plt.show()

