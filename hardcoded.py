#!/usr/bin/env python

'''
hardcoded.py: Imposes hardcoded restrictions on the PMRA and PMDEC of a reduced CSV to remove outliers in the
              Vector Point Diagram.

              This removes obvious outliers from the VPD, which produces a better gaussian fit on the data
              histograms and improves the accuracy of the minimum spanning tree algorithm. A new CSV is
              produced so that it can be used for other files without having to continuously enforce the data
              restrictions
'''

# imports
import pandas as pd

__author__ = 'Rik Ghosh'
__copyright__ = 'Copyright 2021, The University of Texas at Austin'
__credits__ = ['Katherine Clark', 'Soham Saha', 'Mihir Suvarna']
__license__ = 'MIT'
__version__ = '1.2.4'
__maintainer__ = 'Rik Ghosh'
__email__ = 'rikghosh487@gmail.com'
__status__ = 'Development'

def main():
    # reading statistically reduced datafile
    df = pd.read_csv('reduced.csv')

    # hardcoded data reductions
    df = df[(df['pmra'] > -15) & (df['pmra'] < 11.5)]
    df = df[(df['pmdec'] > -15) & (df['pmdec'] < 10)]

    df.to_csv('restricted.csv', index=False)

if __name__ == '__main__':
    main() 
