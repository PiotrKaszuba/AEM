import matplotlib.pyplot as plt


def visualizeData(position_data, nodes, edges, retFigure=False, drawEdges=True):
    fig = plt.figure()
    fig.add_subplot()
    c = ['#DF0174', 'r', 'g', 'b', 'c', 'm', 'y', '#3B240B', '#FF4000', '#0A0A2A', '#5A8E0A', '#CF4557', '#7FA537',
         '#747899', '#dc982f', '#373a03', 'k', '#732f26', '#b99356', '#92daa9']
    i = 0
    for nodeSet in nodes:
        plt.scatter(position_data[nodeSet, 0], position_data[nodeSet, 1], c=c[i % len(c)], zorder=10)
        i += 1
    if drawEdges:
        for edge in edges:
            edge = list(edge)
            inds = position_data[edge[:2]]
            plt.plot(inds[:, 0], inds[:, 1], 'k', lw=2)

    if retFigure:
        return fig
    else:
        plt.show()


import numpy as np
import cv2


def draw(position_data, nodes, edges):
    fig = visualizeData(position_data, nodes,
                        edges, True)
    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    cv2.imshow('win', data)
    cv2.waitKey(10)
    plt.close(fig)
