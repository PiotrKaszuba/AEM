from time import time

from Code.Data.DistanceMatrix import getDistanceMatrix
from Code.Data.LoadData import readData
from Code.Methods.Nearest import Nearest
import random
# start time measure
t = time()
# prepare data
position_data = readData()
matrix = getDistanceMatrix(position_data)
all_nodes = len(position_data)
clusters = 10
times = 100

optimal_nearest = None
optimal_length = None
optimal_seed = 0
for loop in range(times):
    seed = time()
    random.seed(seed)
    nearest = Nearest(range(len(matrix)), matrix, clusters, init_by_range=True, online_draw=False,
                      position_data=position_data)
    #nearest.visualize(position_data)

    for i in range(all_nodes - clusters):
        nearest.distribute_optimal_point()

    current_length = nearest.sum_of_MST()
    print('Time: ' + str(time() - t))
    t = time()

    if optimal_length is None or optimal_length > current_length:
        optimal_length = current_length
        optimal_nearest = nearest
        optimal_seed = seed
        with open('max.txt', 'w') as file:
            file.write('Seed: ' +str(optimal_seed)+', Length: '+str(optimal_length))

    print(str(loop + 1) + '. Sum of lengths: ' + str(current_length))
    # nearest.visualize(position_data)
print('-----------------------------')
print('Best sum of lengths: ' + str(optimal_length))
print('Time: ' + str(time() - t))
optimal_nearest.visualize(position_data)
# length, edges = PRIM.PRIM(nodes, matrix)
# length2, edges2 = PRIM.PRIM(nodes2, matrix)
# print(length)
# print(MST_length(nodes, matrix))
# print elapsed time

# visualizeData(position_data, [nodes,nodes2], edges+ edges2)
