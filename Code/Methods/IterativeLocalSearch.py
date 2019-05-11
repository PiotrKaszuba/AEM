from Code.Methods.LocalSearch import LocalSearch
import time
import numpy as np
class IterativeLocalSearach:
    def __init__(self,nearest, useCache, useCandidateMoves, distance_matrix, k_candidates):
        self.useCache = useCache
        self.useCandidateMoves =useCandidateMoves
        self.distance_matrix =distance_matrix
        self.k_candidates = k_candidates
        self.localSearch = LocalSearch(nearest._clusters, nearest, useCache=useCache, useCandidateMoves=useCandidateMoves, distance_matrix=distance_matrix, k_candidates=k_candidates)
        self.nearest = nearest
        self.timeToGo = 100

    def multiple_start_local_search(self):
        pass

    def iterative_local_search(self):
        currentTime = 0
        while(True):
            start =time.time()
            self.localSearch.greedy()
            if currentTime>self.timeToGo:
                break
            self.destroy()
            self.repair()
            end = time.time()
            currentTime += end-start
        pass

    def destroy(self, destroy_ratio=1.0, method='random'):
        number_of_points = len(self.nearest._distance_matrix)
        if method == 'random':
            to_delete = np.random.choice(range(number_of_points), int(number_of_points * destroy_ratio))
            for point in to_delete:
                self.nearest._nodes_left.append(point)
                graph = self.localSearch.graphFromPoint[point]
                graph.removePoints(points=None, point=point)

    def repair(self,random = False):
        while (len(self.nearest._nodes_left) > 0):
            if(random):
                self.nearest.distribute_random_point()
            else:
                self.nearest.distribute_next_point()
            self.localSearch = LocalSearch(self.nearest._clusters, self.nearest, useCache=self.useCache,useCandidateMoves=self.useCandidateMoves, distance_matrix=self.distance_matrix,k_candidates=self.k_candidates)


