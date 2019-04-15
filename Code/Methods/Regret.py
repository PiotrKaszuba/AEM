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
import math


class Regret:
    def __init__(self, nodes, distance_matrix, rand, num_of_clusters=None, starting_points=None, init_by_range=False,
                 online_draw=False, position_data=None):
        self._distance_matrix = distance_matrix
        self._nodes_left = list(nodes)
        self._num_of_clusters = num_of_clusters
        self._online_draw = online_draw
        self._position_data = position_data
        self._random = rand;
        assert bool(num_of_clusters is None) ^ bool(starting_points is None)  # xor
        if starting_points is None:
            self._clusters = self.initialize_by_range() if init_by_range else self.initialize_random()
        else:
            self._clusters = [
                Graph(
                    list(point), distance_matrix)
                for point in starting_points
            ]
        for i in range(len(self._clusters)):
            self._clusters[i].id = i

    def initialize_random(self):
        return [
            Graph(
                [self._nodes_left.pop(
                    self._random.randrange(
                        len(self._nodes_left)
                    )
                )], self._distance_matrix)
            for _ in range(self._num_of_clusters)
        ]

    def func(self, x):
        # x -= random.randrange(140,160)
        # return -(x ** 2) + random.randrange(75,90) * x

        # negative 'a' coeff in quadratic function gives it's max at -b/2a
        # let max be at calculated product distance -> -b/2a = product -> b = -2* a * product
        # slope initialized at a = 1 -> increasing / decrasing modifies the slope
        # c might be set to get some threshold
        a = - abs(self._slope_level)  # a is negative and at slope level
        b = -2 * a * self._product
        c = self._threshold
        f = a * (x ** 2) + b * x + c

        return f

    def initialize_by_range(self):
        dims = len(self._position_data[0])
        self._product = 1
        for i in range(dims):
            min_i = np.amin(self._position_data[:, i - 1], axis=0)
            max_i = np.amax(self._position_data[:, i - 1], axis=0)
            rang_i = max_i - min_i
            self._product *= rang_i

        self._product /= self._num_of_clusters
        # root of dims degree
        self._product = math.pow(self._product, 1 / dims)
        self._product *= math.sqrt(dims)  # times diagonal

        self._slope_level = 1
        self._threshold = 0

        # indices = np.unravel_index(np.argmax(self._distance_matrix), self._distance_matrix.shape)
        # points = [ind for ind in indices]

        points = [self._random.randint(0, 201)]

        while len(points) < self._num_of_clusters:
            candidates = [([self._distance_matrix[i, point] for point in points], i) for i in
                          range(len(self._distance_matrix)) if i not in points]

            cand_vals = [(mean(list(map(self.func, cand[0])))  # - var(self._distance_matrix[:, cand[1]])
                          , cand[1]) for
                         cand in candidates]

            sum_dist, point = max(cand_vals, key=lambda t: t[0])
            points.append(point)
        self._nodes_left = [node for node in self._nodes_left if node not in points]
        return [Graph([points[i]], self._distance_matrix) for i in range(self._num_of_clusters)]

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
        point = self._nodes_left.pop(self._random.randrange(0, len(self._nodes_left)))
        costs = [(graph.get_node_cost(point), graph) for graph in self._clusters]
        cost, graph = min(costs, key=lambda t: t[0])
        if len(self._nodes_left) > 0:
            concurrent_graph, point2 = self.get_concurrent_graph()
            if  concurrent_graph == graph or concurrent_graph.get_node_cost(point) >= cost:
                graph.appendPoint(point)
            if concurrent_graph.get_node_cost(point) < cost:
                # print("Regret used")
                # concurrent_graph.appendPoint(point)
                self._nodes_left.append(point)
            concurrent_graph.removePoints([point2], True)
        else:
            graph.appendPoint(point)
        if self._online_draw:
            self.draw()

    def get_concurrent_graph(self):
        point = self._nodes_left[self._random.randrange(0, len(self._nodes_left))]
        costs = [(graph.get_node_cost(point), graph) for graph in self._clusters]
        cost, graph = min(costs, key=lambda t: t[0])
        graph.appendPoint(point)
        return graph, point

    def visualize(self, position_data):
        visualizeData(position_data, [graph.points for graph in self._clusters],
                      reduce(add, [graph.edges for graph in self._clusters]))

    def sum_of_MST(self):
        return reduce(add, [graph.MST_length for graph in self._clusters])
