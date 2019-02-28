import numpy as np


def PRIM(nodes, distance_matrix, getOnlySum=False):
    if len(nodes) < 2:
        if getOnlySum:
            return 0
        return 0, []
    if len(nodes) == 2:
        dist = distance_matrix[nodes[0], nodes[1]]
        print(dist)
        if getOnlySum:
            return dist
        return dist, [(nodes[0], nodes[1], dist)]
    nodes_in = [nodes[0]]
    nodes_left = nodes[1:]
    edges = []
    sum = 0
    while len(nodes_left) > 0:
        node_in, node_left, dist = chooseMinDist(nodes_in, nodes_left, distance_matrix)
        nodes_in.append(node_left)
        nodes_left.remove(node_left)
        edges.append((node_in, node_left, dist))
        sum += dist
        if len(nodes_left) == 0:
            print(dist)
    if getOnlySum:
        return sum

    return sum, edges


def chooseMinDist(nodes_in, nodes_left, distance_matrix):
    local_matrix = distance_matrix[nodes_in][:, nodes_left]
    flat = np.argmin(local_matrix)
    indices = np.unravel_index(flat, local_matrix.shape)

    return nodes_in[indices[0]], nodes_left[indices[1]], local_matrix[indices]
