from random import shuffle
import math

class LocalSearch:
    def __init__(self, listOfGraphs, nearest=None):
        self.graphs = listOfGraphs
        self.points = []
        self.graphFromPoint = self.generatePointsDict()

        self.metric = self.countMetric(True)
        self.nearest = nearest
    def countMetric(self, recompute=False):
        temp = 0
        weights = 0
        for graph in self.graphs:
            if recompute:
                graph.full_connected_graph_point_distance()
            temp += graph.points_distance if not math.isnan(graph.points_distance) else 0
            weights += graph.weights
        self.metric = temp / weights
        return self.metric

    def generatePointsDict(self):
        self.graphFromPoint = {}
        for graph in self.graphs:
            for point in graph.points:
                self.graphFromPoint[point] = graph
                self.points.append(point)
        return self.graphFromPoint
    def draw(self):
        self.nearest.draw()
    def generateMoves(self):
        self.moves = []
        for point in self.points:
            for graph in self.graphs:
                if graph != self.graphFromPoint[point]:
                    self.moves.append((point, graph))

        shuffle(self.moves)

    def moveCost(self, point, graphFrom, graphTo):
        currentCostGraphFrom = (graphFrom.points_distance,graphFrom.weights)
        currentCostGraphTo = (graphTo.points_distance,graphTo.weights)
        before = self.countMetric()
        changedCostFrom, changedCostTo = self.movePoint(point, graphFrom, graphTo, True)
        after = self.countMetric()
        self.movePoint(point, graphTo, graphFrom, avgs_to_set=[currentCostGraphTo, currentCostGraphFrom])





        return before - after, changedCostFrom, changedCostTo

    def movePoint(self, point, graphFrom, graphTo, recompute=False, avgs_to_set=None):
        graphFrom.removePoints([point], False)
        graphTo.appendPoint(point, False)
        if recompute:
            graphFrom.full_connected_graph_point_distance()
            graphTo.full_connected_graph_point_distance()
        if avgs_to_set is not None:
            graphFrom.points_distance = avgs_to_set[0][0]
            graphFrom.weights = avgs_to_set[0][1]
            graphTo.points_distance = avgs_to_set[1][0]
            graphTo.weights = avgs_to_set[1][1]
        return (graphFrom.points_distance,graphFrom.weights), (graphTo.points_distance,graphTo.weights)

    def greedyStep(self):
        for move in self.moves:
            point = move[0]
            currentGraph = self.graphFromPoint[point]
            moveToGraph = move[1]

            move_cost, sum_from, sum_to =  self.moveCost(point, currentGraph, moveToGraph)

            if move_cost > 0:

                self.movePoint(point, currentGraph, moveToGraph, avgs_to_set=[sum_from, sum_to])
                self.graphFromPoint[point] = moveToGraph
                return True

        return False


    def greedy(self):
        improve = True

        while (improve):
            print("Step")
            self.generateMoves()
            improve = self.greedyStep()
            print(self.countMetric(True))
            self.draw()

    def steep_step(self):
        max_move = 0
        best_move = None;
        for move in self.moves:
            point = move[0]
            currentGraph = self.graphFromPoint[point]
            moveToGraph = move[1]

            move_cost, sum_from, sum_to = self.moveCost(point, currentGraph, moveToGraph)
            if move_cost > max_move:
                max_move = move_cost
                best_move = (move, sum_from, sum_to)
        if(best_move!=None):
            self.movePoint(best_move[0][0],self.graphFromPoint[best_move[0][0]],best_move[0][1],avgs_to_set=[sum_from,sum_to])
            self.graphFromPoint[best_move[0][0]] = best_move[0][1]
            return True
        else:
            return False
        

    def steep(self):
        improve = True
        while (improve):
            self.generateMoves()
            improve = self.steep_step()
