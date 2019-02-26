import matplotlib.pyplot as plt
def visualizeData(position_data, nodes, edges):
    plt.scatter(position_data[nodes, 0], position_data[nodes, 1], c=['r'], zorder=10)
    for edge in edges:
        edge = list(edge)
        plt.plot(position_data[edge[:2]][:, 0], position_data[edge[:2]][:, 1], 'k', lw=2)

    plt.show()