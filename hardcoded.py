#!/usr/bin/env python

'''
hardcoded.py: Imposes hardcoded restrictions on the PMRA and PMDEC of a reduced CSV to remove outliers in the
              Vector Point Diagram. Also extracts 38.3% of all datapoints from the mean of the parallax

              This removes obvious outliers from the VPD, which produces a better gaussian fit on the data
              histograms and improves the accuracy of the minimum spanning tree algorithm. A new CSV is
              produced so that it can be used for other files without having to continuously enforce the data
              restrictions
'''

# imports
import pandas as pd
import numpy as np

__author__ = 'Rik Ghosh'
__copyright__ = 'Copyright 2021, The University of Texas at Austin'
__credits__ = ['Katherine Clark', 'Soham Saha', 'Mihir Suvarna']
__license__ = 'MIT'
__version__ = '1.2.5'
__maintainer__ = 'Rik Ghosh'
__email__ = 'rikghosh487@gmail.com'
__status__ = 'Production'

# globals
UPPER = 10
LOWER = -15
FACTOR = 0.5

def main():
    # reading statistically reduced datafile
    df = pd.read_csv('reduced.csv')

    # hardcoded data reductions
    df = df[(df['pmra'] > LOWER) & (df['pmra'] < UPPER)]
    df = df[(df['pmdec'] > LOWER) & (df['pmdec'] < UPPER)]

    # Taking 38.3% of the data from parallax
    meanp = np.mean(df['parallax'])
    stdp = np.std(df['parallax'])

    df = df[(df['parallax'] >= meanp - FACTOR * stdp) & (df['parallax'] <= meanp + FACTOR * stdp)]

    # new CSV with row indices being ignored
    df.to_csv('restricted.csv', index=False)

if __name__ == '__main__':
    main() 
