import csv
import glob
from collections import defaultdict
from datetime import datetime

import numpy as np
import pytz
from matplotlib import pyplot as plt

dir_name = 'russian-troll-tweets-master/'


def get_tweet_times():
    counts = defaultdict(int)

    for name in glob.iglob('russian-troll-tweets-master/*.csv'):
        print(name)
        with open(name, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                naive_dt = datetime.strptime(row[5], '%m/%d/%Y %H:%M')
                utc_dt = pytz.utc.localize(naive_dt)
                pst = pytz.timezone('America/Los_Angeles')
                pst_dt = utc_dt.astimezone(pst)
                hour = pst_dt.hour + int(round(pst_dt.minute / 60))
                counts[hour] += 1

    return counts


def main():
    counts = get_tweet_times()
    print(sum(counts.values()))
    x, y = zip(*sorted(counts.items()))

    fig, ax = plt.subplots()
    plt.plot(x, y, color=(0,0,1,0.3), linewidth=1, marker='.', markeredgecolor=(0,0,1,1), markerfacecolor=(0,0,1,1), markersize=20)

    x_lines = [12]
    for xc in x_lines:
        plt.axvline(x=xc, color=(0,0,0,0.5), linestyle='--')

    x_ticks = np.arange(0, 24, 4.0)
    plt.xticks(x_ticks, " ")
    # plt.yticks([])
    # plt.savefig("fig.png", dpi=320)
    plt.show()


if __name__ == "__main__":
    main()
