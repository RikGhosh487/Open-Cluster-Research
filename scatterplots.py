# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# function to produce scatterplots
def scatterplot(dataframe, param1, param2, title):
    # Retrieve display data
    axis1 = param1['axis']
    label1 = param1['name']
    axis2 = param2['axis']
    label2 = param2['name']

    # generate plot
    plt.scatter(dataframe[label1], dataframe[label2], marker='.', label='data')
    plt.xlabel(axis1)
    plt.ylabel(axis2)
    plt.legend(loc='best')
    plt.title(f'{title} Scatterplot')
    plt.show()

def main():
    # Reading datafile and dropping missing fields
    df = pd.read_csv('results.csv').dropna()

    # Statistical Data Reductions
    df = df[df['pmra_error'] < 1]
    df = df[df['pmdec_error'] < 1]

    # GAIA parallax correction
    df = df[df['parallax'] >= 0]

    # Scatterplots
    scatterplot(df, dict(name='ra', axis=r'$\alpha$' + ' (deg)'),
            dict(name='dec', axis=r'$\delta$' + ' (deg)'), 'Structure in ICRS')
    scatterplot(df, dict(name='pmra', axis=r'$\mu_{\alpha*} cos(\delta)$' + ' (mas/yr)'),
            dict(name='pmdec', axis=r'$\mu_{\delta}$' + ' (mas/yr)'), 'Vector Point Diagram')

if __name__ == '__main__':
    main()