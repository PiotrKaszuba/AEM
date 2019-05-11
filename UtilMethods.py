import numpy as np

def destroy(nearest, number_of_points, destroy_ratio, localsearch, method='random' ):
    if method=='random':
        to_delete = np.random.choice(range(number_of_points), int(number_of_points*destroy_ratio))
        for point in to_delete:
            nearest._nodes_left.append(point)
            graph = localsearch.graphFromPoint[point]
            graph.removePoints(points=None, point=point)



