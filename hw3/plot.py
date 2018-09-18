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

    plt.axhline(y=golden_ratio, alpha=0.5, label='\u03c6')
    plt.axhline(y=math.pi, alpha=0.5, color='orange', label='\u03c0')

    plt.plot(x, y_phi, marker='.', markersize=10)
    plt.plot(x, y_pi, marker='.', markersize=10)

    plt.title("Simple Continued Fractions for \u03c0 and \u03c6")
    plt.xlabel("n")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig("fig.png", dpi=320)

if __name__ == "__main__":
    main()
