#!/usr/bin/env python

'''
clean.py: Takes a CSV file and extracts a new CSV with statistical data reductions.

          A dataframe is created from the CSV. The dataframe undergoes statistical data reductions
          for a certain ERROR_THRESHOLD. The reduced dataframe is then converted to a new CSV for
          future use.
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

# main function
def main():
    # constants
    FILENAME = r'./csv/raw_data.csv'
    ERROR_THRESHOLD = 0.5

    # dataframe creation
    df = pd.read_csv(FILENAME)
    df = df.dropna()

    # standard error removal
    df = df[(df['pmra_error'] < ERROR_THRESHOLD) & (df['pmdec_error'] < ERROR_THRESHOLD)]
    df = df[(df['ra_error'] < ERROR_THRESHOLD) & (df['dec_error'] < ERROR_THRESHOLD)]
    df = df[df['parallax'] < ERROR_THRESHOLD]

    # CSV creation
    df.to_csv('./csv/err_rm.csv', index=False)

if __name__ == '__main__':
    main()
