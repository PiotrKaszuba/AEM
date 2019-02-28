from time import time

from DistanceMatrix import getDistanceMatrix
from LoadData import readData
from Nearest import Nearest

# start time measure
t = time()
# prepare data
position_data = readData()
matrix = getDistanceMatrix(position_data)
all_nodes = len(position_data)
clusters = 10
times = 10

optimal_nearest = None
optimal_length = None
for loop in range(times):

    nearest = Nearest(range(len(matrix)), matrix, clusters)

    for i in range(all_nodes - clusters):
        nearest.distribute_optimal_point()

    current_length = nearest.sum_of_MST()


    if optimal_length is None or optimal_length > current_length:
        optimal_length = current_length
        optimal_nearest = nearest
    print(str(loop+1) + '. Sum of lengths: ' + str(current_length))
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
