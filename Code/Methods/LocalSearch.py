from random import shuffle
import math
import numpy as np
import time

class LocalSearch:
    def __init__(self, listOfGraphs, nearest=None, useCandidateMoves=False, useCache=False, distance_matrix=None,
                 k_candidates=10):
        self.graphs = listOfGraphs
        self.points = []
        self.graphFromPoint = {}
        self.generatePointsDict()
        self.metric = self.countMetric(True)
        self.nearest = nearest
        self.useCandidateMoves = useCandidateMoves
        self.useCache = useCache
        self.candidateMoves = self.generateCandidatesForPoints(distance_matrix, k_candidates)
        self.cache_array = np.full((len(listOfGraphs), len(listOfGraphs), len(self.points), 2, 2), np.nan)
        self.moves_done = {}

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
        #x = [(graph.points_distance, graph.weights) for graph in self.graphs]
        if setVar:
            self.metric = temp / weights
            return self.metric
        else:
            return temp / weights

    def generatePointsDict(self):
        for graph in self.graphs:
            for point in graph.points:
                self.graphFromPoint[point] = graph
                self.points.append(point)
        return self.graphFromPoint

    def draw(self, saveFile=None):
        self.nearest.draw(saveFile)

    def generateMoves(self):
        self.moves = []
        #t = time.time()
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
        # print(len(self.moves))

        shuffle(self.moves)
        #print(time.time() - t)

    def testForCost(self, point ,graphFrom, graphTo):
        # zapamietanie aktualnego stanu

        currentCostGraphFrom = (graphFrom.points_distance, graphFrom.weights)
        currentCostGraphTo = (graphTo.points_distance, graphTo.weights)

        # testowanie przeniesienia punktu
        changedCostFrom, changedCostTo = self.movePoint(point, graphFrom, graphTo, True)

        # obliczenie metryki wlasciwe
        after = self.countMetric(setVar=False)

        # odwracamy efekt testów
        self.movePoint(point, graphTo, graphFrom, avgs_to_set=[currentCostGraphTo,
                                                               currentCostGraphFrom])  # uzupelniajac zapamietanym stanem poprzednim

        if self.useCache:
            self.updateCache(graphFrom, graphTo, point, changedCostFrom, changedCostTo)

        return after, changedCostFrom, changedCostTo

    def testForCostWithCache(self, graphFrom, graphTo, cacheVal):
        currentCostGraphFrom = (graphFrom.points_distance, graphFrom.weights)
        currentCostGraphTo = (graphTo.points_distance, graphTo.weights)
        graphFrom.points_distance = cacheVal[0][0]
        graphFrom.weights = cacheVal[0][1]
        graphTo.points_distance = cacheVal[1][0]
        graphTo.weights = cacheVal[1][1]

        after = self.countMetric(setVar=False)
        graphFrom.points_distance = currentCostGraphFrom[0]
        graphFrom.weights = currentCostGraphFrom[1]
        graphTo.points_distance = currentCostGraphTo[0]
        graphTo.weights = currentCostGraphTo[1]
        return after



    def moveCost(self, point, graphFrom, graphTo):
        if not self.useCache:
           after, changedCostFrom, changedCostTo = self.testForCost(point, graphFrom, graphTo)

        else:
            cacheVal = self.getFromCache(graphFrom, graphTo, point)
            if np.isnan(cacheVal).any():
                after, changedCostFrom, changedCostTo = self.testForCost(point, graphFrom, graphTo)
            else:
                after = self.testForCostWithCache(graphFrom, graphTo, cacheVal)

                #print(after)
                changedCostFrom = cacheVal[0]
                changedCostTo = cacheVal[1]
        # zwracamy roznice w poprzednim stanie a nowym, oba skladniki ( dla grafu from i to) i nowa metryke
        return self.metric - after, changedCostFrom, changedCostTo, after

    def movePoint(self, point, graphFrom, graphTo, recompute=False, avgs_to_set=None):
        graphFrom.removePoints(points=None, point=point, compute_MST=False)

        graphTo.appendPoint(point, False)

        if recompute:
            graphFrom.full_connected_graph_point_distance(computeAll=False, pointRemove=point)
            graphTo.full_connected_graph_point_distance(computeAll=False, pointAdd=point)

        if avgs_to_set is not None:
            graphFrom.points_distance = avgs_to_set[0][0]
            graphFrom.weights = avgs_to_set[0][1]
            graphTo.points_distance = avgs_to_set[1][0]
            graphTo.weights = avgs_to_set[1][1]
        return (graphFrom.points_distance, graphFrom.weights), (graphTo.points_distance, graphTo.weights)

    def greedyStep(self):


        for move in self.moves:

            point = move[0]
            currentGraph = self.graphFromPoint[point]
            moveToGraph = move[1]

            move_cost, sum_from, sum_to, metricAfter = self.moveCost(point, currentGraph, moveToGraph)

            if move_cost > 0:

                self.movePoint(point, currentGraph, moveToGraph, avgs_to_set=[sum_from, sum_to])

                if self.useCache:
                    self.updateCacheAfterMove(currentGraph, moveToGraph)

                self.graphFromPoint[point] = moveToGraph
                self.metric = metricAfter

                return True

        return False

    # def greedyStep2(self):
    #
    #
    #     while True:
    #         move = self.generateMove()
    #         if move == False:
    #             print("ff")
    #             self.generateMoves()
    #             self.moves_done.clear()
    #             return self.greedyStep()
    #
    #         point = move[0]
    #         currentGraph = self.graphFromPoint[point]
    #         moveToGraph = move[1]
    #
    #         move_cost, sum_from, sum_to, metricAfter = self.moveCost(point, currentGraph, moveToGraph)
    #
    #         if move_cost > 0:
    #             print("ok")
    #             self.movePoint(point, currentGraph, moveToGraph, avgs_to_set=[sum_from, sum_to])
    #
    #             if self.useCache:
    #                 self.updateCacheAfterMove(currentGraph, moveToGraph)
    #
    #             self.graphFromPoint[point] = moveToGraph
    #             self.metric = metricAfter
    #             self.moves_done.clear()
    #             return True

    # def generateMove(self):
    #     for i in range(1000):
    #         point = self.nearest._random.randint(0, len(self.points)-1)
    #         graph = self.nearest._random.randint(0, len(self.graphs)-1)
    #         accept = False
    #         if self.moves_done.get((point,graph)) is None and self.graphFromPoint[point] != self.graphs[graph]:
    #             accept=True
    #             if self.useCandidateMoves:
    #                 accept=False
    #             for pt in self.candidateMoves[point]:
    #                 if self.graphs[graph] == self.graphFromPoint[pt]:
    #                     accept=True
    #                     break
    #         if accept:
    #             self.moves_done[(point, graph)] = True
    #             return (point, self.graphFromPoint[graph])
    #     return False


    def greedy(self):
        improve = True

        while (improve):
            # print("Step")

            self.generateMoves()
            improve = self.greedyStep()
            #print(self.countMetric())
            #print(time.time()-t)
            # self.draw()
        #print([self.timer1, self.timer2, self.timer3, self.timer4, self.timer5])
    def steep_step(self):
        max_move = 0
        best_move = None
        best_after = None

        for move in self.moves:

            # print(len(self.moves))

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
            self.movePoint(best_move[0][0], self.graphFromPoint[best_move[0][0]], best_move[0][1],
                           avgs_to_set=[best_move[1], best_move[2]])
            if self.useCache:
                self.updateCacheAfterMove(self.graphFromPoint[best_move[0][0]], best_move[0][1])
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
            # print(self.countMetric(True))
            improve = self.steep_step()

            # print("Step")
            # self.countMetric(True)
            # print()
            # self.draw()

    def updateCache(self, move_from, move_to, point, sum_from, sum_to):
        self.cache_array[move_from.id, move_to.id, point] = (sum_from, sum_to)

    def updateCacheAfterMove(self, move_from, move_to):
        #self.cache_array[:] = np.nan
        self.cache_array[move_from.id] = np.nan
        self.cache_array[move_to.id] = np.nan
        self.cache_array[:, move_from.id] = np.nan
        self.cache_array[:, move_to.id] = np.nan


    def getFromCache(self,move_from,move_to,point):
        index = (move_from.id,move_to.id,point)
        return self.cache_array[index]
