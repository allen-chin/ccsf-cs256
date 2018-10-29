"""Snippet code to generate income distributions by zip code in San Francisco"""

import re
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

def get_first_day():
    df = pd.read_csv("access_log.csv")
    df['date'] = df['date'].astype('datetime64')

    dates = df['date']
    start_date = np.datetime64('2018-08-27T00:00:00-0700')
    end_date = np.datetime64('2018-08-28T00:00:00-0700')
    mask = (dates > start_date) & (dates < end_date)
    first_day = dates[mask]
    first_day.columns = ["date"]

    # Issue exists where the timezone is applied to the timestamp
    first_day.to_csv("first_day.csv", index=False)
    return first_day

def plot_all_days():
    df = pd.read_csv("access_log.csv")
    df['date'] = pd.to_datetime(df['date'])

    # Plot other statistics
    counts = df['date'].groupby([df['date'].dt.date, df['date'].dt.hour]).count()
    counts = counts.unstack(level=1)

    counts.iloc[1].plot(label='Other Accesses', legend=True, color='#e7bc9a', alpha=1, marker='o')
    for _, row in counts.iterrows():
        if row.max() < 400:
            row.plot(color='#e7bc9a', alpha=0.1, linestyle='', marker='o')

    counts.mean().plot(label='Mean', legend=True, marker='o')
    # counts.min().plot()
    # counts.max().plot()

def main():
    # generate_data_file()
    # get_first_day()
    plot_all_days()
    first_day = pd.read_csv("first_day.csv")
    first_day['date'] = pd.to_datetime(first_day['date'])
    first_day['date'] = first_day['date'].dt.tz_localize('UTC')
    first_day['date'] = first_day['date'].dt.tz_convert('US/Pacific')
    first_day['date'].groupby([first_day['date'].dt.hour]).count().plot(label='First Day of Instruction', legend=True, color='#0000ff', marker='o')

    plt.title('CCSF hills Server Access on First Day of Instruction', fontsize=40)
    # plt.xticks(ticks=np.arange(0, 24, 1), labels=None)
    plt.xlabel('Hour of Day (PST)', fontsize=24)
    plt.ylabel('Number of Accesses', fontsize=24)
    plt.show()

if __name__ == "__main__":
    main()
