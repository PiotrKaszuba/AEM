from time import time

from DistanceMatrix import getDistanceMatrix
from LoadData import readData
from drawGraph import visualizeData
import PRIM
from MST import MST_length
import random
# start time measure
t = time()
#prepare data
position_data = readData()
matrix = getDistanceMatrix(position_data)

nodes = random.sample(range(201), 20)
length, edges = PRIM.PRIM(nodes, matrix)

print(length)
print(MST_length(nodes, matrix))
# print elapsed time
print(str(time() - t))
visualizeData(position_data, nodes, edges)