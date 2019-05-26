from Code.Methods.LocalSearch import  LocalSearch
from itertools import combinations, chain
import numpy as np
from scipy.stats import pearsonr, linregress
import math
import pickle
import matplotlib.pyplot as plt
from Code.localSearchSimilaritiesRunner import localSearchRunner
def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)

#https://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    return diffprod / math.sqrt(xdiff2 * ydiff2)

def run():
    best, solutions = localSearchRunner()
    results = correlationSimilarity(best, solutions)
    print(results)
    with open("correlations.bin", mode='wb') as file:
        pickle.dump(results, file)
    with open("correlations.txt", mode='w') as file:
        file.write(str(results))

def load():
    with open("correlations.bin", mode='rb') as file:
        results = pickle.load(file)
    ind = np.argmin(results[7])
    print(results[6][ind])
    print(results[7][ind])
    scores = results[6]
    print(np.mean(scores))
    similarities = results[7]
    scipyPearson = pearsonr(similarities, scores)
    scipyLineregress = linregress(similarities, scores)
    numpyCorr = np.corrcoef(scores, similarities)
    stackDefinition = pearson_def(scores, similarities)
    print(scipyPearson)
    print(scipyLineregress)
    plt.scatter(similarities, scores)
    abline(scipyLineregress[0], scipyLineregress[1])
    plt.show()
    #print(np.mean(results[7]))

def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--', c='g')
    plt.xlabel("Podobieństwo")
    plt.ylabel("Koszt")
    plt.title("Liniowa zależność kosztu od podobieństwa do rozwiązania najlepszego")
def correlationSimilarity(best : LocalSearch, solutions):
    divisor = getDivisor(best)
    scores = np.array([solution.metric for solution in solutions])
    similarities = np.array(list(map(lambda x: x/divisor, [compareSimilarity(best, solution) for solution in solutions])))

    scipyPearson = pearsonr(scores, similarities)
    scipyLineregress = linregress(scores, similarities)
    numpyCorr = np.corrcoef(scores, similarities)
    stackDefinition = pearson_def(scores, similarities)

    return [scipyPearson, scipyLineregress, numpyCorr, stackDefinition, best.metric, divisor, scores, similarities]





def getPairsOfPointsFromSolution(localsearch : LocalSearch):
    return chain.from_iterable(combinations(graph.points, 2) for graph in localsearch.graphs)


def getDivisor(best : LocalSearch):
    return sum([graph.weights for graph in best.graphs])



def compareSimilarity(best : LocalSearch, compared : LocalSearch):
    pairGenerator = getPairsOfPointsFromSolution(best)
    similarity = 0
    for pair in pairGenerator:
        if compared.graphFromPoint[pair[0]] == compared.graphFromPoint[pair[1]]:
            similarity += 1
    return similarity

if __name__ == "__main__":
    load()

