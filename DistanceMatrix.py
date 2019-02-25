from scipy.spatial.distance import cdist


def getDistanceMatrix(data):
    return cdist(data, data, 'euclidean')
