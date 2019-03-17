import random
from time import time

from scipy import average

from Code.Data.DistanceMatrix import getDistanceMatrix
from Code.Data.LoadData import readData
from Code.Methods.Nearest import Nearest
from Code.Methods.Regret import Regret

# prepare data
position_data = readData(path="../objects.data")
matrix = getDistanceMatrix(position_data)
all_nodes = len(position_data)
clusters = 10
times = 100

optimal_nearest = None
optimal_length = None
optimal_seed = 0
lengths = []
durations = []
seed = 7
random.seed(seed)

rand = random.Random();
rand.seed(4)
for loop in range(times):

    t = time()
    nearest = Regret(range(len(matrix)), matrix, rand, clusters, init_by_range=True, online_draw=False, position_data=position_data)
    # nearest = Nearest(range(len(matrix)), matrix, rand, clusters, init_by_range=False, online_draw=False, position_data=position_data)
    # nearest.visualize(position_data)

    while(len(nearest._nodes_left)>0):
        nearest.distribute_next_point()

    current_length = nearest.sum_of_MST()

    duration = time() - t
    print('Time: ' + str(duration))
    durations.append(duration)

    lengths.append(current_length)


    if optimal_length is None or optimal_length > current_length:
        optimal_length = current_length
        optimal_nearest = nearest
        optimal_seed = seed

    print(str(loop + 1) + '. Sum of lengths: ' + str(current_length))

    # nearest.visualize(position_data)

print('-----------------------------')
print('Best sum of lengths: ' + str(optimal_length))
print('Worst: ' + str(max(lengths)))
print('Avg: ' + str(average(lengths)))
print('Avg Time: ' + str(average(durations)))
with open('max.txt', 'a+') as file:
    file.write('Seed: ' + str(optimal_seed) + ', Best: ' + str(optimal_length) + ', Worst: ' + str(max(
        lengths)) + ', Avg: ' + str(average(lengths)) + ', Avg time: ' + str(average(durations)) + '\n')
optimal_nearest.visualize(position_data)
# length, edges = PRIM.PRIM(nodes, matrix)
# length2, edges2 = PRIM.PRIM(nodes2, matrix)
# print(length)
# print(MST_length(nodes, matrix))
# print elapsed time

# visualizeData(position_data, [nodes,nodes2], edges+ edges2)
