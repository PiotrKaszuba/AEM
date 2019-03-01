from itertools import combinations

import networkx as nx
from networkx import minimum_spanning_tree


def MST_length(nodes, distanceMatrix):
    G = nx.Graph()
    #nodes are represented as indexes from distance matrix
    G.add_nodes_from(nodes)
    #create all combinations of 2 nodes (all pairs) and append their distance -> list of lists of u,v,weight
    lst = [list(combination) + [(distanceMatrix[combination[0], combination[1]])] for combination in
           combinations(nodes, 2)]
    G.add_weighted_edges_from(lst)
    MST = minimum_spanning_tree(G)
    return MST.size(weight='weight')
