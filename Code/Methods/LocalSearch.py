from random import shuffle
import math
import numpy as np
class LocalSearch:
    def __init__(self, listOfGraphs, nearest=None, useCandidateMoves=False, useCache=False, distance_matrix = None, k_candidates=10):
        self.graphs = listOfGraphs
        self.points = []
        self.graphFromPoint = self.generatePointsDict()
        self.metric = self.countMetric(True)
        self.nearest = nearest
        self.useCandidateMoves = useCandidateMoves
        self.useCache = useCache
        self.candidateMoves = self.generateCandidatesForPoints(distance_matrix, k_candidates)

    def generateCandidatesForPoints(self, distance_matrix, k):
        idx = np.argpartition(distance_matrix, k)
        return idx[:, :k]
    def countMetric(self, recompute=False, setVar=True):
        temp = 0
        weights = 0
        for graph in self.graphs:
            if recompute:
                graph.full_connected_graph_point_distance()
            temp += graph.points_distance if not math.isnan(graph.points_distance) else 0
            weights += graph.weights
        if setVar:
            self.metric = temp / weights
            return self.metric
        else:
            return temp/weights

    def generatePointsDict(self):
        self.graphFromPoint = {}
        for graph in self.graphs:
            for point in graph.points:
                self.graphFromPoint[point] = graph
                self.points.append(point)
        return self.graphFromPoint
    def draw(self, saveFile = None):
        self.nearest.draw(saveFile)
    def generateMoves(self):
        self.moves = []
        for point in self.points:
            if self.useCandidateMoves:
                graphsSet = {self.graphFromPoint[pt] for pt in self.candidateMoves[point]}
                for graph in graphsSet:
                    if graph != self.graphFromPoint[point]:
                        self.moves.append((point, graph))
            else:
                for graph in self.graphs:
                    if graph != self.graphFromPoint[point]:
                        self.moves.append((point, graph))
        #print(len(self.moves))
        shuffle(self.moves)

    def moveCost(self, point, graphFrom, graphTo):

        currentCostGraphFrom = (graphFrom.points_distance,graphFrom.weights)
        currentCostGraphTo = (graphTo.points_distance,graphTo.weights)


        changedCostFrom, changedCostTo = self.movePoint(point, graphFrom, graphTo, True)

        after = self.countMetric(setVar=False)

        self.movePoint(point, graphTo, graphFrom, avgs_to_set=[currentCostGraphTo, currentCostGraphFrom])





        return self.metric - after, changedCostFrom, changedCostTo, after

    def movePoint(self, point, graphFrom, graphTo, recompute=False, avgs_to_set=None):
        graphFrom.removePoints(points= None, point = point, compute_MST= False)

        graphTo.appendPoint(point, False)


        if recompute:
            graphFrom.full_connected_graph_point_distance(computeAll=False, pointRemove=point)
            graphTo.full_connected_graph_point_distance(computeAll=False, pointAdd = point)

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

            move_cost, sum_from, sum_to, metricAfter =  self.moveCost(point, currentGraph, moveToGraph)

            if move_cost > 0:

                self.movePoint(point, currentGraph, moveToGraph, avgs_to_set=[sum_from, sum_to])
                self.graphFromPoint[point] = moveToGraph
                self.metric = metricAfter
                return True

        return False


    def greedy(self):
        improve = True

        while (improve):
            #print("Step")
            self.generateMoves()
            improve = self.greedyStep()
            #print(self.countMetric(True))
            #self.draw()

    def steep_step(self):
        max_move = 0
        best_move = None
        best_after = None

        for move in self.moves:

            #print(len(self.moves))

            point = move[0]
            currentGraph = self.graphFromPoint[point]
            moveToGraph = move[1]

            move_cost, sum_from, sum_to, metricAfter = self.moveCost(point, currentGraph, moveToGraph)

            if move_cost > max_move:
                #print(self.countMetric(True))
                max_move = move_cost
                best_move = (move, sum_from, sum_to)
                best_after = metricAfter

        if best_move is not None:
            self.movePoint(best_move[0][0],self.graphFromPoint[best_move[0][0]],best_move[0][1],avgs_to_set=[best_move[1],best_move[2]])
            self.graphFromPoint[best_move[0][0]] = best_move[0][1]
            self.metric = best_after
            #self.countMetric()

            return True
        else:
            return False
        

    def steep(self):
        improve = True
        while (improve):
            self.generateMoves()
            #print(self.countMetric(True))
            improve = self.steep_step()
            #print("Step")
            #self.countMetric(True)
            #print()
            #self.draw()