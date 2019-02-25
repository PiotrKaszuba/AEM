import csv

import numpy as np


def readData(path='objects.data'):
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter=' ')
        data = [[int(row[0]), int(row[1])] for row in reader]
    return np.array(data)
