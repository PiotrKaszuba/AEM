import matplotlib.pyplot as plt
def visualizeData(position_data, nodes, edges):
    c = ['#DF0174', 'r', 'g', 'b', 'c', 'm', 'y', '#3B240B', '#FF4000', '#0A0A2A']
    i = 0
    for nodeSet in nodes:
        plt.scatter(position_data[nodeSet, 0], position_data[nodeSet, 1], c=c[i%len(c)], zorder=10)
        i+=1

    for edge in edges:
        edge = list(edge)
        inds = position_data[edge[:2]]
        plt.plot(inds[:, 0], inds[:, 1], 'k', lw=2)


    plt.show()