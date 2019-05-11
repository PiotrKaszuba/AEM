from Code.Methods.LocalSearch import LocalSearch
import time

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

    def destroy(self):
        pass

    def repair(self,random = False):
        while (len(self.nearest._nodes_left) > 0):
            if(random):
                self.nearest.distribute_random_point()
            else:
                self.nearest.distribute_next_point()
            self.localSearch = LocalSearch(self.nearest._clusters, self.nearest, useCache=self.useCache,useCandidateMoves=self.useCandidateMoves, distance_matrix=self.distance_matrix,k_candidates=self.k_candidates)


