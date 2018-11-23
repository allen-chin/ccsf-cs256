import matplotlib.pyplot as plt
import networkx as nx


def main():
    graph = nx.Graph()
    graph.add_node("California")



    nx.draw(graph)
    plt.show()


if __name__ == "__main__":
    main()