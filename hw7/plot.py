"""Snippet code to generate income distributions by zip code in San Francisco"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def clean_data():
    incomes = pd.read_excel('ca-income.xls', header=2, names=['Income', 'Count'], index_col=0, usecols=[0, 1, 2], skiprows=[0], skip_blank_lines=True)
    incomes = incomes.dropna()
    incomes.index.name = "Zip"

    zip_codes = get_zips()
    incomes.loc[zip_codes].to_csv('sf-income.csv')

def get_zips():
    zip_codes = pd.read_csv('san-francisco-zip-codes.csv')
    return sorted(zip_codes['zip'].unique())

cache = {}
def get_sum(incomes, zip_code):
    if zip_code not in cache:
        cache[zip_code] = sum(incomes.loc[zip_code]['Count'])

    return cache[zip_code]


def label_frequency(incomes, row):
    return 100 * row['Count'] / get_sum(incomes, row.name)

def main():
    # clean_data()
    incomes = pd.read_csv('sf-income.csv', index_col=0)

    fig, axes = plt.subplots(nrows=5, ncols=6, sharex=True, sharey=True)
    fig.suptitle("Gross Income Distribution in San Francisco by Zip Code", fontsize=24)
    fig.text(0.5, 0.04, 'Income Brackets in Thousand Dollars', ha='center', fontsize=24)
    fig.text(0.04, 0.5, 'Population Percent', va='center', rotation='vertical', fontsize=24)

    fig.subplots_adjust(hspace=0.5)
    fig.delaxes(axes[4][3])
    fig.delaxes(axes[4][4])
    fig.delaxes(axes[4][5])

    for i, zip_code in enumerate(get_zips()):
        incomes['Frequency'] = incomes.apply (lambda row: label_frequency(incomes, row), axis=1)

        row, col = np.unravel_index(i, axes.shape)
        ax = axes[row][col]
        incomes.loc[zip_code].plot(x='Income', y='Frequency', ax=ax, marker='.', markersize=10)

        ax.xaxis.label.set_visible(False)
        ax.set_title(zip_code)
        ax.set_xticklabels(['0', '25', '50', '75', '100', '200', '200+'])
        # ax.set_yticks([])
        ax.legend().remove()
        ax.grid(True, axis='y')

    plt.show()


if __name__ == "__main__":
    main()
