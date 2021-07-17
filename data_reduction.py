#!/usr/bin/env python

'''
data_reduction.py: Takes a CSV file and extracts a new CSV with statistical data reductions and adjustments.
                   
                   Pandas is used to read a CSV into a dataframe. The dataframe is reduced so that all the
                   elements have a pmra_error < 1, pmdec_error < 1, and parallax >= 0. Pandas is again used to 
                   convert the reduced dataframe to a CSV named reduced.csv
'''

# imports
import pandas as pd

__author__ = 'Rik Ghosh'
__copyright__ = 'Copyright 2021, The University of Texas at Austin'
__credits__ = ['Katherine Clark', 'Soham Saha', 'Mihir Suvarna']
__license__ = 'MIT'
__version__ = '1.0.1'
__maintainer__ = 'Rik Ghosh'
__email__ = 'rikghosh487@gmail.com'
__status__ = 'Production'

def main():
    # read the CSV and drop missing fields
    df = pd.read_csv('raw_data.csv').dropna()

    # statistical data reductions
    df = df[(df['pmra_error'] < 1) & (df['pmdec_error'] < 1)]
    
    # GAIA parallax adjustment
    df = df[df['parallax'] >= 0]

    # new CSV with row indices being ignored
    df.to_csv('reduced.csv', index=False)

if __name__ == '__main__':
    main()
