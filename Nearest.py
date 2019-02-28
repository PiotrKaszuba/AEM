import random
from functools import reduce
from operator import add

import numpy as np

from Graph import Graph
from drawGraph import visualizeData


class Nearest:
    def __init__(self, nodes, distance_matrix, num_of_clusters=None, starting_points=None):
        self._distance_matrix = distance_matrix
        self._nodes_left = list(nodes)
        assert bool(num_of_clusters is None) ^ bool(starting_points is None)  # xor
        if starting_points is None:
            self._clusters = [
                Graph(
                    [self._nodes_left.pop(
                        random.randrange(
                            len(self._nodes_left)
                        )
                    )], distance_matrix)
                for _ in range(num_of_clusters)
            ]

        else:
            self._clusters = [
                Graph(
                    list(point), distance_matrix)
                for point in starting_points
            ]

    def get_min_point_to_add_to_clusters(self):
        temp = list()
        for graph in self._clusters:
            graph.compute_nodes_costs(self._nodes_left)
            min_cost_node, min_cost = graph.get_min_cost_node_and_cost()
            temp.append((min_cost, min_cost_node, graph))

        ind = np.argmin(list(zip(*temp))[0])  # when nested iterables - returns minimum of first positions
        return temp[ind]

    def distribute_optimal_point(self):
        _, min_cost_node, graph= self.get_min_point_to_add_to_clusters()
        graph.appendPoint(min_cost_node)
        for cluster in self._clusters:
            cluster.pop_from_candidates(min_cost_node)
        self._nodes_left.remove(min_cost_node)

    def visualize(self, position_data):
        visualizeData(position_data, [graph.points for graph in self._clusters],
                      reduce(add, [graph.edges for graph in self._clusters]))

    def sum_of_MST(self):
        return reduce(add, [graph.MST_length for graph in self._clusters])
