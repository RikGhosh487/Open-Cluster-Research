# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# function to produce histogram
def histogram(dataframe, field, bins):
    # Retrieve display data
    axis = field['axis']
    label_name = field['name']

    # Generate plot
    hist, bins, _ = plt.hist(dataframe[field['name']], bins, histtype='step')

    # Statistics for Gaussian Model
    mean = np.mean(dataframe[label_name])
    std = np.std(dataframe[label_name])
    p = norm.pdf(bins, mean, std)

    # Plotting Gaussian fit
    plt.plot(bins, p / p.sum() * len(dataframe), 'r--', label='Gaussian Fit')
    plt.xlabel(axis)
    plt.ylabel('Count')
    plt.legend(loc='best')
    plt.title(f'{label_name.upper()} Histogram')
    plt.show()

def main():
    # Reading datafile and dropping missing fields
    df = pd.read_csv('results.csv').dropna()

    # Statistical Data Reductions
    df = df[df['pmra_error'] < 1]
    df = df[df['pmdec_error'] < 1]

    # GAIA Parallax Correction
    df = df[df['parallax'] >= 0]

    # Histograms
    histogram(df, dict(name='ra', axis=r'$\alpha$' + ' (deg)'), 50)
    histogram(df, dict(name='dec', axis=r'$\delta$' + ' (deg)'), 50)
    histogram(df, dict(name='pmra', axis=r'$\mu_{\alpha*} cos(\delta)$' + ' (mas/yr)'), 50)
    histogram(df, dict(name='pmdec', axis=r'$\mu_{\delta}$' + ' (mas/yr)'), 50)
    histogram(df, dict(name='parallax', axis=r'$\pi$' + ' (mas)'), 50)

if __name__ == '__main__':
    main()