#!/usr/bin/env python

'''
scatterplots.py: Produces matplotlib scatterplots for major two-dimensional properties of a CSV.
                 
                 Matplotlib is used for its TEX support
'''

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'Rik Ghosh'
__copyright__ = 'Copyright 2021, The University of Texas at Austin'
__credits__ = ['Katherine Clark', 'Soham Saha', 'Mihir Suvarna']
__license__ = 'MIT'
__version__ = '1.3.1'
__maintainer__ = 'Rik Ghosh'
__email__ = 'rikghosh487@gmail.com'
__status__ = 'Production'

# function to produce scatterplots
def scatterplot(dataframe, param1, param2, title, reverse=False):
    # Retrieve display data
    axis1 = param1['axis']
    label1 = param1['name']
    axis2 = param2['axis']
    label2 = param2['name']

    # generate plot
    plt.scatter(dataframe[label1], dataframe[label2], marker='.', label='data')
    if(reverse):
        plt.gca().invert_yaxis()
    plt.xlabel(axis1)
    plt.ylabel(axis2)
    plt.legend(loc='best')
    plt.title(f'{title} Scatterplot')
    plt.show()

def main():
    # Reading datafile
    df = pd.read_csv('restricted.csv')

    # Scatterplots
    scatterplot(df, dict(name='ra', axis=r'$\alpha$' + ' (deg)'),
            dict(name='dec', axis=r'$\delta$' + ' (deg)'), 'Structure in ICRS')
    scatterplot(df, dict(name='pmra', axis=r'$\mu_{\alpha*} cos(\delta)$' + ' (mas/yr)'),
            dict(name='pmdec', axis=r'$\mu_{\delta}$' + ' (mas/yr)'), 'Vector Point Diagram')
    scatterplot(df, dict(name='bp_rp', axis=r'$B_P - R_P$' + ' (mag)'),
            dict(name='phot_g_mean_mag', axis=r'$G$' + ' (mag)'), 'Color Magnitude Diagram', True)

if __name__ == '__main__':
    main()