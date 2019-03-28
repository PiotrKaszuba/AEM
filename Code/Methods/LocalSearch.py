from random import shuffle


class LocalSearch:
    def __init__(self, listOfGraphs):
        self.graphs = listOfGraphs
        self.points = []
        self.graphFromPoint = self.generatePointsDict()

        self.metric = self.countMetric(True)

    def countMetric(self, recompute=False):
        temp = 0
        for graph in self.graphs:
            if recompute:
                graph.full_connected_graph_avg_point_distance()
            temp += graph.avg_points_distance
        self.metric = temp / len(self.graphs)

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
        changesCostFrom, changedCostTo = self.movePoint(point, graphFrom, graphTo, True)

        self.movePoint(point, graphTo, graphFrom, avgs_to_set=)

        graphFrom.avg_points_distance = currentCostGraphFrom
        graphTo.avg_points_distance = currentCostGraphTo

        avgBefore = (currentCostGraphFrom + currentCostGraphTo) / 2
        avgAfter = (changedCostFrom + changedCostTo) / 2

        return avgBefore - avgAfter, changedCostFrom, changedCostTo

    def movePoint(self, point, graphFrom, graphTo, recompute=False, avgs_to_set=None):
        graphFrom.remove([point], False)
        graphTo.appendPoint(point, False)
        if recompute:
            graphFrom.full_connected_graph_avg_point_distance()
            graphTo.full_connected_graph_avg_point_distance()
        if avgs_to_set is not None:
            graphFrom.avg_points_distance = avgs_to_set[0]
            graphTo.avg_points_distance = avgs_to_set[1]
        return graphFrom.avg_points_distance, graphTo.avg_points_distance

    def greedyStep(self):
        for move in self.moves:
            point = move[0]
            currentGraph = self.graphFromPoint[point]
            moveToGraph = move[1]

            move_cost, avg_from, avg_to =  self.moveCost(point, currentGraph, moveToGraph)

            if move_cost > 0:


    def greedy(self):
        improve = True

        while (improve):
            self.generateMoves()
            self.greedyStep()

    def steep_step(self):
        max_move = 0
        best_move = None;
        for move in self.moves:
            point = move[0]
            currentGraph = self.graphFromPoint[point]
            moveToGraph = move[1]

            move_cost, avg_from, avg_to = self.moveCost()
            if move_cost > max_move:
                max_move = move_cost
                best_move = (move, avg_from, avg_to)
        if(best_move!=None):
            self.movePoint(best_move[0][0],self.graphFromPoint[best_move[0][0]],best_move[0][1],avgs_to_set=[avg_from,avg_to])
            return True
        else:
            return False
        

    def steep(selfs):
        improve = True
        while (improve):
            self.generateMoves()
            improve = self.steep_step()
