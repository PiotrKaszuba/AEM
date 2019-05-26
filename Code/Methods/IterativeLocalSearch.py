from Code.Methods.LocalSearch import LocalSearch
import time
import numpy as np
import copy as cp
from Code.Methods.Nearest import  Nearest
class IterativeLocalSearach:
    def __init__(self,nearest, useCache, useCandidateMoves, distance_matrix, k_candidates, destroy_bonus_growth=0.0, randRepair = True):
        self.useCache = useCache
        self.useCandidateMoves =useCandidateMoves
        self.distance_matrix =distance_matrix
        self.k_candidates = k_candidates
        self.localSearch = LocalSearch(nearest._clusters, nearest, useCache=useCache, useCandidateMoves=useCandidateMoves, distance_matrix=distance_matrix, k_candidates=k_candidates)
        self.nearest = nearest
        self.bestResult = None
        self.bestInstance = None
        self.destroy_bonus = 0.0
        self.destroy_bonus_growth = destroy_bonus_growth
        self.randRepair = randRepair
    def draw(self, name, drawEdges):
        self.bestInstance.draw(name, drawEdges)
    # def multiple_start_local_search(self):
    #     pass
    #multiple start when destroy ratio = 1.0
    def iterative_local_search(self,destroy_ratio=1.0,max_iters=100,tineToGo=None):
        currentTime = 0
        iters= 0
        start = time.time()
        while(True):

            self.localSearch.greedy()
            iters += 1
            print(str(iters) + ": Time: " + str(time.time() - start))

            value = self.localSearch.countMetric()
            print(str(iters) + ": Time: " + str(time.time() - start) + ", Value: " + str(value))

            if self.bestResult is not None:
                if value < self.bestResult:
                    self.bestResult = value
                    self.bestInstance = cp.deepcopy(self.nearest)
                    self.destroy_bonus = 0.0
                else:
                    self.destroy_bonus += self.destroy_bonus_growth
                    self.nearest = cp.deepcopy(self.bestInstance)
                    self.localSearch = LocalSearch(self.nearest._clusters, self.nearest, useCache=self.useCache, useCandidateMoves=self.useCandidateMoves, distance_matrix=self.distance_matrix, k_candidates=self.k_candidates)
            else:
                self.bestResult = value
                self.bestInstance = cp.deepcopy(self.nearest)
            end = time.time()
            currentTime += end - start
            start = time.time()
            print(currentTime)
            if (tineToGo is not None and currentTime>tineToGo) or (tineToGo is None and iters == max_iters):
                break
            self.destroy(destroy_ratio=destroy_ratio)
            self.repair(self.randRepair)


        return self.localSearch.countMetric()

    def destroy(self, destroy_ratio=1.0, method='random'):
        number_of_points = len(self.nearest._distance_matrix)
        if method == 'random':
            to_delete = np.random.choice(range(number_of_points), int(number_of_points * min(1, min(2*destroy_ratio, destroy_ratio+self.destroy_bonus))),replace=False)
            for point in to_delete:
                self.nearest._nodes_left.append(point)
                graph = self.localSearch.graphFromPoint[point]
                graph.removePoints(points=None, point=point)

    def repair(self,rand = True):
        # import random
        # nearest = Nearest(range(len(self.distance_matrix)), self.distance_matrix,  random.Random(), 20,
        #                   init_by_range=False, online_draw=False,
        #                   position_data=self.nearest._position_data, nearest_obj=self.nearest)
        # self.nearest = nearest
        if not rand:
            self.nearest.recompute_all()
        while (len(self.nearest._nodes_left) > 0):
            if(rand):
                self.nearest.distribute_random_point()
            else:
                self.nearest.distribute_next_point_new_metric()
        # self.localSearch.points = []
        # self.localSearch.graphFromPoint.clear()
        # self.localSearch.generatePointsDict()
        # self.localSearch.countMetric(True)

        self.localSearch = LocalSearch(self.nearest._clusters, self.nearest, useCache=self.useCache,useCandidateMoves=self.useCandidateMoves, distance_matrix=self.distance_matrix,k_candidates=self.k_candidates)


