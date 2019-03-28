from random import shuffle
class LocalSearch:
    def __init__(self, listOfGraphs):
        self.graphs = listOfGraphs
        self.points = []
        self.graphFromPoint = self.generatePointsDict()

        self.metric = self.countMetric()

    def countMetric(self):
        temp=0
        for graph in self.graphs:
            temp+=graph.MST_length
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


    def greedyStep(self):
        for move in self.moves:
            point = move[0]
            currentGraph = self.graphFromPoint[point]



    def greedy(self):
        improve = True

        while(improve):
            self.generateMoves()


