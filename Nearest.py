import random
from operator import sub

import numpy as np

from PRIM import PRIM


def nearest(nodes, distance_matrix):
    nodes = list(nodes)
    starting = np.array([[nodes.pop(random.randrange(len(nodes)))] for _ in range(10)])

    print(nearestForClasses(nodes, starting, distance_matrix))


'''
    f=list(
        map(lambda x:
            list(
                map(lambda y:
                    PRIM(x+[y], distance_matrix, True)
                    , nodes)
            ), starting)
    )

    print(f)
'''


def nearestForClasses(nodes_left, classes, distance_matrix):
    return np.argmin([nearestForClass(nodes_left, _class, distance_matrix) for _class in classes])


def nearestForClass(nodes_left, class_points, distance_matrix):
    ind = np.argmin(
        map(sub,
            [PRIM
             (list(class_points) + [node],
              distance_matrix, True
              )
             for node in nodes_left],
            [PRIM
             (list(class_points),
              distance_matrix, True
              )
             for node in nodes_left]
            )
    )

    return nodes_left[ind],

    # print(starting)
    # print(len(nodes))
