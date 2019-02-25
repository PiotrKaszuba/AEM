from time import time

from DistanceMatrix import getDistanceMatrix
from LoadData import readData
from MST import MST_length

# start time measure
t = time()
data = readData()
matrix = getDistanceMatrix(data)
nodes = range(len(data))
print(MST_length(nodes, matrix))
# print elapsed time
print(str(time() - t))
