from functools import reduce
from operator import add
from operator import itemgetter

from Code.PRIM import PRIM
from Code.drawGraph import draw

from itertools import combinations
import numpy as np

import math
class Graph:
    def __init__(self, points, distance_matrix):
        self.points = points
        self._recompute = True
        self.MST_length = 0
        self._candidate_nodes_costs = {}
        self._distance_matrix = distance_matrix
        self.points_distance = 0;

        self.edges = []
        self.computeMST()

    def computeMST(self):
        self.MST_length, self.edges = PRIM(self.points, self._distance_matrix)

    def appendPoint(self, node, compute_MST=True):
        self.points.append(node)
        self._recompute = True
        if compute_MST:
            self.computeMST()

    def removePoints(self, points, compute_MST=False):
        self.points = [point for point in self.points if point not in points]
        self._recompute = True
        if compute_MST:
            self.computeMST()

    def compute_edges_length(self):
        return reduce(add, [i[2] for i in self.edges])

    def get_node_cost(self, node):
        return PRIM(
            list(self.points) + [node],
            self._distance_matrix,
            True
        ) - self.MST_length

    def compute_nodes_costs(self, nodes):
        if self._recompute:
            self._candidate_nodes_costs.clear()
            self._candidate_nodes_costs = {
                node: PRIM(
                    list(self.points) + [node],
                    self._distance_matrix,
                    True
                ) - self.MST_length
                for node in nodes}
            self._recompute = False

    def get_min_cost_node_and_cost(self):
        key = min(self._candidate_nodes_costs, key=self._candidate_nodes_costs.get)
        return key, self._candidate_nodes_costs[key]

    def pop_from_candidates(self, node):
        self._candidate_nodes_costs.pop(node)

    def _remove_edge(self, edge_endpoints0, edge_endpoints1):
        self.edges = [i for i in self.edges if not (i[0] in edge_endpoints0 and i[1] in edge_endpoints1)]

    def get_max_edge(self):
        return max(self.edges, key=itemgetter(2))

    def remove_edge(self, edges):
        for edge in edges:
            self._remove_edge([edge[0], edge[1]], [edge[0], edge[1]])

    def get_first_connected_subgraph(self, points_data=None):
        if len(self.edges) == 0:
            return [self.points[0]]
        edge_in = self.edges[0]
        points_in = set([edge_in[0], edge_in[1]])

        edges_in = [edge_in]

        edges_left = self.edges[1:]
        edges_wait = [edge for edge in edges_left if edge[0] in points_in or edge[1] in points_in]
        edges_left = [left for left in edges_left if left not in edges_wait]
        while (len(edges_wait) > 0):
            edge_current = edges_wait.pop(0)
            edges_in.append(edge_current)
            points_in.add(edge_current[0])
            points_in.add(edge_current[1])

            edges_wait += [edge for edge in edges_left if edge[0] in points_in or edge[1] in points_in]
            edges_left = [left for left in edges_left if left not in edges_wait]
            if points_data is not None:
                draw(points_data, [list(points_in)], edges_in)

        self.edges = edges_left

        return list(points_in)

    def nCr(self, n, k):
        if n-k < 0:
            return 0
        f = math.factorial
        return f(n) / f(k) / f(n - k)
    def full_connected_graph_point_distance(self):

        self.points_distance = np.sum([self._distance_matrix[pair] for pair in combinations(self.points, 2)])

        self.weights = self.nCr(len(self.points), 2)
        return self.points_distance
