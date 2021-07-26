#!/usr/bin/env python

'''
data_reductions.py: Takes 1 standard deviation error margin for each of the 5 parameters of GAIA Astrometry

                    A dataframe is created from a CSV and then 68% of the observations are extracted from
                    the 5  parameters of the GAIA Astrometry. The resulting dataframe is then converted
                    to a new CSV for future use.
'''

# imports
import pandas as pd
import numpy as np

__author__ = 'Rik Ghosh'
__copyright__ = 'Copyright 2021, The University of Texas at Austin'
__credits__ = ['Katherine Clark', 'Soham Saha', 'Mihir Suvarna']
__license__ = 'MIT'
__version__ = '1.0.1'
__maintainer__ = 'Rik Ghosh'
__email__ = 'rikghosh487@gmail.com'
__status__ = 'Production'

# main function
def main():
    # constants
    FILENAME = r'./csv/reduced.csv'

    # dataframe
    df = pd.read_csv(FILENAME)

    # PMRA
    m = np.mean(df['pmra'])
    s = np.std(df['pmra'])
    df = df = df[(df['pmra'] <= m + s) & (df['pmra'] >= m - s)]

    # PMDEC
    m = np.mean(df['pmdec'])
    s = np.std(df['pmdec'])
    df = df[(df['pmdec'] <= m + s) & (df['pmdec'] >= m - s)]

    # PARALLAX
    m = np.mean(df['parallax'])
    s = np.std(df['parallax'])
    df = df[(df['parallax'] <= m + s) & (df['parallax'] >= m - s)]

    df.to_csv('./csv/stat_adj.csv', index=False)

if __name__ == '__main__':
    main()
