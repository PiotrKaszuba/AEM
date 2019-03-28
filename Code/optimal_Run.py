from Code.Graph import Graph
from Code.Data.DistanceMatrix import getDistanceMatrix
from Code.Data.LoadData import readData
from Code.drawGraph import  visualizeData
from functools import reduce
from operator import add
position_data = readData(path="../objects.data")
matrix = getDistanceMatrix(position_data)
all_nodes = len(position_data)



g = Graph(list(range(all_nodes)), matrix)
edges_cut = []
# cutting max edges
for i in range(9):
    edges_cut.append(g.get_max_edge())
    g.remove_edge([edges_cut[i]])
print(g.compute_edges_length())
graphs = []
visualizeData(position_data, [g.points],
                  g.edges)
# building clusters from disconnected graphs
for i in range(10):
    points = g.get_first_connected_subgraph()
    g.removePoints(points)
    graphs.append(Graph(points, matrix))

    visualizeData(position_data, [graphs[i].points],
                  graphs[i].edges)



visualizeData(position_data, [graph.points for graph in graphs],
              reduce(add, [graph.edges for graph in graphs]))

