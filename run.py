from time import time

from DistanceMatrix import getDistanceMatrix
from LoadData import readData
from drawGraph import visualizeData
import PRIM
from MST import MST_length
import Nearest
import random
# start time measure
t = time()
#prepare data
position_data = readData()
matrix = getDistanceMatrix(position_data)

nodes = random.sample(range(201), 3)
nodes2 = random.sample(range(201), 3)

Nearest.nearest(range(201), matrix)
#length, edges = PRIM.PRIM(nodes, matrix)
#length2, edges2 = PRIM.PRIM(nodes2, matrix)
#print(length)
#print(MST_length(nodes, matrix))
# print elapsed time
print(str(time() - t))
#visualizeData(position_data, [nodes,nodes2], edges+ edges2)