from random import shuffle
class LocalSearch:
    def __init__(self, listOfGraphs):
        self.graphs = listOfGraphs
        self.points = []
        self.graphFromPoint = self.generatePointsDict()

        self.metric = self.countMetric(True)

    def countMetric(self, recompute=False):
        temp=0
        for graph in self.graphs:
            if recompute:
                graph.full_connected_graph_avg_point_distance()
            temp+=graph.average_points_distance
        self.metric = temp/len(self.graphs)
    def generatePointsDict(self):
        for graph in self.graphFromPoint:
            for point in graph.points:
                self.graphFromPoint[point] = graph
                self.points.append(point)

    def generateMoves(self):
        self.moves = []
        for point in self.points:
            for graph in self.graphs:
                if graph != self.graphFromPoint[point]:
                    self.moves.append((point, graph))

        shuffle(self.moves)

    def moveCost(self, point, graphFrom, graphTo):
        currentCostGraphFrom = graphFrom.average_points_distance
        currentCostGraphTo = graphTo.average_points_distance
        graphFrom.remove(point, False)
    def greedyStep(self):
        for move in self.moves:
            point = move[0]
            currentGraph = self.graphFromPoint[point]
            self.moveCost()


    def greedy(self):
        improve = True

        while(improve):
            self.generateMoves()
            self.greedyStep()

