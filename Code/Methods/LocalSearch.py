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
            temp+=graph.avg_points_distance
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
        currentCostGraphFrom = graphFrom.avg_points_distance
        currentCostGraphTo = graphTo.avg_points_distance
        graphFrom.remove([point], False)
        graphTo.appendPoint(point, False)
        changedCostFrom = graphFrom.full_connected_graph_avg_point_distance()
        changedCostTo = graphTo.full_connected_graph_avg_point_distance()
        graphTo.remove([point], False)
        graphFrom.appendPoint(point, False)

        graphFrom.avg_points_distance = currentCostGraphFrom
        graphTo.avg_points_distance = currentCostGraphTo

        avgBefore = (currentCostGraphFrom+currentCostGraphTo)/2
        avgAfter = (changedCostFrom+changedCostTo)/2

        return avgBefore - avgAfter, changedCostFrom, changedCostTo


    def greedyStep(self):
        for move in self.moves:
            point = move[0]
            currentGraph = self.graphFromPoint[point]
            moveToGraph = move[1]

            move_cost, avg_from, avg_to =  self.moveCost()


    def greedy(self):
        improve = True

        while(improve):
            self.generateMoves()
            self.greedyStep()

