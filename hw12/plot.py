import random

import matplotlib.pyplot as plt
import numpy as np

def plot(array):
    X = array[:, 0]
    Y = array[:, 1]
    heatmap, xedges, yedges = np.histogram2d(array[:, 0], array[:, 1], bins=10, normed=True)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]


    plt.clf()
    im = plt.imshow(heatmap.T, cmap="Oranges", extent=extent, origin="lower", aspect="auto", alpha=0.5)

    # Shows frequency right now which is not desirable
    # cbar = plt.colorbar(im, ax=plt.gca())
    # cbar.set_label("Points visited", rotation=-90, va="bottom")
    plt.plot(X, Y, c="black", alpha=0.5)

    plt.scatter([0], [0], label="Start Point", s=40)
    plt.scatter([X[-1]], [Y[-1]], c="black", label="End Point", s=40)
    plt.plot([0, X[-1]], [0, Y[-1]])

    plt.title("Unbounded Random Walk in 2 Dimensions", fontsize=24)
    plt.axis("scaled")
    plt.legend()
    plt.tight_layout()
    plt.show()

def random_walk(n=10000, bound=0):
    x = 0
    y = 0

    for i in range(n):
        yield (x, y)
        dx, dy = random_direction()

        while bound > 0 and (x + dx > bound or x + dx < -bound or y + dy > bound or y + dy < -bound):
            dx, dy = random_direction()

        x += dx
        y += dy


DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]

def random_direction():
    return random.choice(DIRECTIONS)

def main():
    array = np.array(list(random_walk()))
    plot(array)

if __name__ == "__main__":
    main()