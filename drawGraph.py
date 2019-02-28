import matplotlib.pyplot as plt
def visualizeData(position_data, nodes, edges):
    c = ['#eFe24f', 'r', 'g', 'b', 'c', 'm', 'y' ]
    i = 0
    for nodeSet in nodes:
        plt.scatter(position_data[nodeSet, 0], position_data[nodeSet, 1], c=c[i%len(c)], zorder=10)
        i+=1

    for edge in edges:
        edge = list(edge)
        plt.plot(position_data[edge[:2]][:, 0], position_data[edge[:2]][:, 1], 'k', lw=2)


    plt.show()