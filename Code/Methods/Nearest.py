import random
from functools import reduce
from operator import add

import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import mean
from scipy import var

from Code.Graph import Graph
from Code.drawGraph import visualizeData


class Nearest:
    def __init__(self, nodes, distance_matrix, num_of_clusters=None, starting_points=None, init_by_range=False,
                 online_draw=False, position_data=None):
        self._distance_matrix = distance_matrix
        self._nodes_left = list(nodes)
        self._num_of_clusters = num_of_clusters
        self._online_draw = online_draw
        self._position_data = position_data
        assert bool(num_of_clusters is None) ^ bool(starting_points is None)  # xor
        if starting_points is None:
            self._clusters = self.initialize_by_range() if init_by_range else self.initialize_random()
        else:
            self._clusters = [
                Graph(
                    list(point), distance_matrix)
                for point in starting_points
            ]

    def initialize_random(self):
        return [
            Graph(
                [self._nodes_left.pop(
                    random.randrange(
                        len(self._nodes_left)
                    )
                )], self._distance_matrix)
            for _ in range(self._num_of_clusters)
        ]

    @staticmethod
    def func(x):
        x -= random.randrange(140,160)
        return -(x ** 2) + random.randrange(75,90) * x

    def initialize_by_range(self):

        indices = np.unravel_index(np.argmax(self._distance_matrix), self._distance_matrix.shape)
        points = [ind for ind in indices]

        while len(points) < self._num_of_clusters:
            candidates = [([self._distance_matrix[i, point] for point in points], i) for i in
                          range(len(self._distance_matrix)) if i not in points]

            cand_vals = [(mean(list(map(self.func, cand[0]))) - var(self._distance_matrix[:, cand[1]]), cand[1]) for
                         cand in candidates]

            sum_dist, point = max(cand_vals, key=lambda t: t[0])
            points.append(point)
        self._nodes_left = [node for node in self._nodes_left if node not in points]
        return [Graph([points[i]], self._distance_matrix) for i in range(self._num_of_clusters)]

    def get_min_point_to_add_to_clusters(self):
        temp = list()
        for graph in self._clusters:
            graph.compute_nodes_costs(self._nodes_left)
            min_cost_node, min_cost = graph.get_min_cost_node_and_cost()
            temp.append((min_cost, min_cost_node, graph))

        ind = np.argmin(list(zip(*temp))[0])  # when nested iterables - returns minimum of first positions
        return temp[ind]

    def draw(self):
        fig = visualizeData(self._position_data, [graph.points for graph in self._clusters] + [self._nodes_left],
                            reduce(add, [graph.edges for graph in self._clusters]), True)
        fig.canvas.draw()
        data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        cv2.imshow('win', data)
        cv2.waitKey(10)
        plt.close(fig)

    def distribute_next_point(self):
        point = self._nodes_left.pop(random.randrange(0, len(self._nodes_left)))
        costs = [(graph.get_node_cost(point), graph) for graph in self._clusters]
        cost, graph = min(costs, key=lambda t: t[0])
        graph.appendPoint(point)
        if self._online_draw:
            self.draw()

    def distribute_optimal_point(self):
        _, min_cost_node, graph = self.get_min_point_to_add_to_clusters()
        graph.appendPoint(min_cost_node)
        for cluster in self._clusters:
            cluster.pop_from_candidates(min_cost_node)
        self._nodes_left.remove(min_cost_node)
        if self._online_draw:
            self.draw()

    def visualize(self, position_data):
        visualizeData(position_data, [graph.points for graph in self._clusters],
                      reduce(add, [graph.edges for graph in self._clusters]))

    def sum_of_MST(self):
        return reduce(add, [graph.MST_length for graph in self._clusters])
