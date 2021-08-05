#!/usr/bin/env python

'''
train_obtain.py: Uses Random Forest Regressor to obtain Photometric Estimates for Spectroscopic Data

                 SDSS filters (ugriz) are used to obtain missing spectroscopic data through photometric
                 approximations. The Machine Learning model is first trained using an existing training
                 data set that contains both Spectroscopic and Photometric Data. Then the model is scored
                 using a test dataset to determine if the model is fit for approximations. Finally, the data
                 with missing Spectroscopic information is fed into the model to estimate the missing values
'''

# imports
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from scipy.stats import gaussian_kde

__author__ = 'Rik Ghosh'
__copyright__ = 'Copyright 2021, The University of Texas at Austin'
__credits__ = ['Soham Saha', 'Mihir Suvarna']
__license__ = 'MIT'
__version__ = '1.0.3'
__maintainer__ = 'Rik Ghosh'
__email__ = 'rikghosh487@gmail.com'
__status__ = 'Production'

# main function
def main():
    # constants
    PRIMARY_FILENAME = r'./csv/segue.csv'
    SECONDARY_FILENAME = r'./csv/sdss_final.csv'
    CPE = 0.75
    OFFSET = 0.25
    TITLE = 'Machine Learning Truth-to-Prediction Plot'
    LABEL = 'One-to-one Regression Line'

    # dataframes
    df = pd.read_csv(PRIMARY_FILENAME)
    df = df.dropna()
    df2 = pd.read_csv(SECONDARY_FILENAME)
    df2 = df2.dropna()

    # extract y values
    feh = np.array(df['feh'])
    df = df.drop(['logg', 'teff', 'feh'], axis='columns')
    
    # photometric estimates
    x_train, x_test, y_train, y_test = train_test_split(df, feh, test_size=0.2)
    model = RandomForestRegressor(n_estimators=163)
    model.fit(x_train, y_train)     # training model
    y_pred = model.predict(x_test)  # predicting with test data

    # density based coloring
    xy = np.vstack([y_test, y_pred])
    z = gaussian_kde(xy)(xy)

    # plotting
    plt.scatter(y_test, y_pred, c=z, marker='.')
    plt.plot(y_test, y_test, 'r-', label=LABEL)
    plt.text(min(y_test), max(y_pred) - OFFSET, f'RMSE: {round(mean_squared_error(y_test, y_pred), 4)}') # RMSE
    y_pls = [CPE + x for x in y_test]     # CPE lines
    plt.plot(y_test, y_pls, 'b--', label='-0.75 dex line')
    plt.plot(y_pls, y_test, 'b--', label='+0.75 dex line')
    diff = abs(y_pred - y_test)
    count = 0
    for elem in diff:
        if elem > CPE:
            count += 1
    plt.text(min(y_test), max(y_pred) - 2 * OFFSET, f'CPER: {round(count / len(y_test), 4)}') # CPER
    plt.xlabel(r'$[Fe/H]_{SSPP}$')
    plt.ylabel(r'$[Fe/H]_{RF}$')
    plt.legend(loc='best')
    plt.title(TITLE)
    plt.show()

    # actual prediction
    y_pred = model.predict(df2)
    print(f'Cluster Metallicity: {np.mean(y_pred)}')
    
if __name__ == '__main__':
    main()
