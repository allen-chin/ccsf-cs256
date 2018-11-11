"""Code to generate first two weeks of instruction.

The functions to generate the data are used as little as possible
"""

import math
import re
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

def generate_data_file():
    data = generate_data()
    clean_data(data)
    export_data(data)

def generate_data():
    with open("access_log", "r") as f:
        data = [re.split(r"[\[\]\"\n]", line) for line in f]

    return data

def clean_data(data):
    # Day/Month abbreviation/Year:Hour:Minute:Second UTC_Offset
    format = "%d/%b/%Y:%H:%M:%S %z"

    for line in data:
        line[0] = line[0][:-5]
        line[1] = datetime.strptime(line[1], format)

def export_data(data):
    df = pd.DataFrame(data=data)
    df = df.drop([2, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], axis=1)
    df.columns = ["ip", "date", "http", "status", "link", "user-agent"]
    # print(df.iloc[0])
    df.to_csv("access_log.csv", index=False, columns=["date", "link", "user-agent"])

def get_first_two_weeks():
    df = pd.read_csv("../data/access_log.csv")
    df["date"] = df["date"].astype("datetime64")

    start_date = np.datetime64("2018-08-18T00:00:00-0700")
    end_date = np.datetime64("2018-09-01T00:00:00-0700")
    mask = (df["date"] > start_date) & (df["date"] < end_date)
    first_two_weeks = df[mask]

    # Issue exists where the timezone is applied to the timestamp
    first_two_weeks.to_csv("first_two_weeks.csv", index=False)
    return first_two_weeks

def plot_all_days():
    df = pd.read_csv("access_log.csv")
    df["date"] = pd.to_datetime(df["date"])

    # Plot other statistics
    counts = df["date"].groupby([df["date"].dt.date, df["date"].dt.hour]).count()
    counts = counts.unstack(level=1)

    counts.iloc[1].plot(label="Other Accesses", legend=True, color="#e7bc9a", alpha=1, marker="o")
    for _, row in counts.iterrows():
        if row.max() < 400:
            row.plot(color="#e7bc9a", alpha=0.1, linestyle="", marker="o")

    counts.mean().plot(label="Mean", legend=True, marker="o")
    # counts.min().plot()
    # counts.max().plot()

def main():
    # generate_data_file()
    # get_first_two_weeks()
    # plot_all_days()


    # Generate data for plotting
    data = pd.read_csv("first_two_weeks.csv")
    data["date"] = pd.to_datetime(data["date"])
    data["date"] = data["date"].dt.tz_localize("UTC")
    data["date"] = data["date"].dt.tz_convert("US/Pacific")
    counts = data["date"].groupby([data["date"].dt.date, data["date"].dt.hour]).count()
    counts = counts.unstack(level=1)
    mean = np.mean(counts.values)
    print(mean)


    # Set up plot
    ax = plt.subplot(111, projection="polar")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_thetagrids(range(0, 360, 15), range(24))
    ax.set_rgrids(range(0, 500, 100), labels=["", "", 200, 300, 400, ""], angle=1)
    ax.set_rlim(0, 500)


    # See https://stackoverflow.com/a/20107592
    # Get density color map
    theta = math.pi / 12 * np.tile(np.arange(24), len(counts.index))
    r = counts.values.ravel()

    x = theta
    y = r
    # Makes no difference...
    # x = np.multiply(r, np.cos(theta))
    # y = np.multiply(r, np.sin(theta))
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)

    # Sort by density so densest points plotted last
    idx = z.argsort()
    r, theta, z = r[idx], theta[idx], z[idx]
    ax.scatter(theta, r, c=z, s=150, alpha=0.7, cmap="winter")
    ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*mean, color='r', linestyle='-')

    print(counts)
    plt.title("CCSF hills Server Access (08/18/2018 to 09/01/2018)")
    plt.xlabel('Hour of Day (PST)')
    plt.show()

if __name__ == "__main__":
    main()
