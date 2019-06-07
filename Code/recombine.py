from Code.Methods.LocalSearch import  LocalSearch
from Code.Graph import  Graph
from Code.Methods.Nearest import Nearest
import numpy as np

def getMinGroup(point, parent1 :LocalSearch, parent2:LocalSearch):
    graphParent1 = parent1.graphFromPoint[point]
    graphParent2 = parent2.graphFromPoint[point]
    return list(set(graphParent1.points) & set(graphParent2.points))

def difference(a,b):
    return list(set(a)-set(b))

def recombine(parent1 : LocalSearch, parent2 : LocalSearch, k=20):
    points = list(range(len(parent1.nearest._distance_matrix)))
    graphs = []
    while(len(graphs) < k):
        point = np.random.choice(points)
        minGroup = getMinGroup(point, parent1, parent2)
        points = difference(points, minGroup)
        graphTemp = Graph(minGroup, parent1.nearest._distance_matrix, len(graphs))
        graphs.append(graphTemp)
    nearest = Nearest(points, parent1.nearest._distance_matrix, None, k, position_data=parent1.nearest._position_data, online_draw=False, createClusters=False, givenClusters=graphs)
    while (len(nearest._nodes_left) > 0):
        nearest.distribute_random_point()
    localSearch = LocalSearch(nearest._clusters, nearest, useCache=False, useCandidateMoves=True, distance_matrix=parent1.nearest._distance_matrix,
                              k_candidates=21)
    localSearch.greedy()
    localSearch.countMetric(True)

    return localSearch





