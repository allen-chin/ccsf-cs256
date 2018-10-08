import itertools
import math

import numpy as np
from matplotlib import pyplot as plt

def calc_partial(denoms, stop):
    res = np.float64(denoms[stop])
    for i in range(stop - 1, -1, -1):
        res = 1 / res + denoms[i]
    return res

def phi(n):
    res = 1
    for i in range(n):
        yield res
        res = 1 + 1 / res

def pi(n):
    with open("b001203.txt", "r") as f:
        denoms = list(itertools.islice((int(line.split()[1]) for line in f), n))

        for i in range(n):
            yield calc_partial(denoms, i)


def main():
    n = 10
    golden_ratio = (1 + 5 ** 0.5) / 2

    x = list(range(n))
    y_phi = list(phi(n))
    y_pi = list(pi(n))

    print(y_phi, y_pi)
    plt.axhline(y=golden_ratio, alpha=0.5, label='\u03c6')
    plt.axhline(y=math.pi, alpha=0.5, color='orange', label='\u03c0')

    # plt.plot(x, y_phi, marker='.', markersize=10)
    # plt.plot(x, y_pi, marker='.', markersize=10)

    plt.title("Approximate value of \u03c0 and \u03c6")
    # plt.xlabel("x")
    plt.ylabel("y")
    plt.xticks([])
    plt.yticks([golden_ratio, math.pi], ['\u03c6 \u2248 1.618', '\u03c0 \u2248 3.142'])
    plt.ylim(0, 4)
    plt.autoscale(enable=False)
    # plt.legend()
    # plt.show()
    plt.savefig("fig-simple.png", dpi=320)

if __name__ == "__main__":
    main()
