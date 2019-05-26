from time import time
from Code.Methods.LocalSearch import  LocalSearch
from Code.Data.DistanceMatrix import getDistanceMatrix
from Code.Data.LoadData import readData
from Code.Methods.Nearest import Nearest

def localSearchRunner():
    # prepare data
    position_data = readData(path="../objects20_06.data")
    matrix = getDistanceMatrix(position_data)
    clusters = 20
    times = 500

    optimal_nearest = None
    optimal_length = None
    solutions = []

    for loop in range(times):

        t = time()
        nearest = Nearest(range(len(matrix)), matrix, None, clusters, init_by_range=False, online_draw=False, position_data=position_data)
        while(len(nearest._nodes_left)>0):
            nearest.distribute_random_point()



        localSearch = LocalSearch(nearest._clusters, nearest, useCache=False, useCandidateMoves=True, distance_matrix=matrix, k_candidates=21)
        localSearch.greedy()

        current_length = localSearch.countMetric()

        duration = time() - t
        print('Time: ' + str(duration))


        if optimal_length is None or optimal_length > current_length:
            optimal_length = current_length
            optimal_nearest = localSearch
        solutions.append(localSearch)
        print(str(loop + 1) + '. Sum of lengths: ' + str(current_length))
    return optimal_nearest, solutions

if __name__ == "__main__":
    localSearchRunner()
