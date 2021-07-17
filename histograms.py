#!/usr/bin/env python

'''
histograms.py: Produces matplotlib histograms for major properties of a CSV with a gaussian fitting.

               The Gaussian Fit is scaled up to be superimposed on top of the produced histograms instead
               of normalizing the histogram to retain the original frequency counts. Matplotlib is used for
               it TEX support and ability to combine multiple plots
'''

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

__author__ = 'Rik Ghosh'
__copyright__ = 'Copyright 2021, The University of Texas at Austin'
__credits__ = ['Katherine Clark', 'Soham Saha', 'Mihir Suvarna']
__license__ = 'MIT'
__version__ = '1.2.4'
__maintainer__ = 'Rik Ghosh'
__email__ = 'rikghosh487@gmail.com'
__status__ = 'Production'

# function to produce histogram
def histogram(dataframe, field, bins):
    # Retrieve display data
    axis = field['axis']
    label_name = field['name']

    # Generate plot
    hist, bins, _ = plt.hist(dataframe[field['name']], bins, histtype='step', label='Counts')

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
    # Reading datafile
    df = pd.read_csv('restricted.csv')

    # Histograms
    histogram(df, dict(name='ra', axis=r'$\alpha$' + ' (deg)'), 50)
    histogram(df, dict(name='dec', axis=r'$\delta$' + ' (deg)'), 50)
    histogram(df, dict(name='pmra', axis=r'$\mu_{\alpha*} cos(\delta)$' + ' (mas/yr)'), 50)
    histogram(df, dict(name='pmdec', axis=r'$\mu_{\delta}$' + ' (mas/yr)'), 50)
    histogram(df, dict(name='parallax', axis=r'$\pi$' + ' (mas)'), 50)

if __name__ == '__main__':
    main()