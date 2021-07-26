#!/usr/bin/env python

'''
db.py: Takes a error reduced CSV and picks optimal cluster with noise removal.

       A Density-Based Spatial Clustering of Applications with Noise (DBSCAN) algorithm
       is used to pick the optimal cluster using the Vector Point Diagram for the dataframe.
       A new CSV is created from the reduced dataframe for future use.
'''

# imports
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from scipy.stats import gaussian_kde
from kneed import KneeLocator

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
    FILENAME = r'./csv/err_rm.csv'
    SAMPLE_SIZE = 50

    # dataframe
    df = pd.read_csv(FILENAME)

    # data extraction
    x = np.array(df['pmra'])
    y = np.array(df['pmdec'])
    X = np.vstack([x, y]).T
    XS = StandardScaler().fit_transform(X)

    # knee determination
    nei = NearestNeighbors(n_neighbors=SAMPLE_SIZE)
    nei_fit = nei.fit(XS)
    distances, _ = nei_fit.kneighbors(XS)
    distances = np.sort(distances, axis=0)
    distances = distances[:, 1]
    i = np.arange(len(distances))
    kneedle = KneeLocator(i, distances, S=1, curve='convex', direction='increasing')
    
    # plotting
    plt.plot(distances)
    plt.axvline(kneedle.knee, color='red', linestyle='--', label='Elbow')
    plt.legend(loc='best')
    plt.xlabel('Datapoints')
    plt.ylabel(r'$\epsilon$')
    plt.title('Elbow Estimation for DBSCAN')
    plt.show()

    # DBSCAN
    db = DBSCAN(eps=kneedle.knee_y, min_samples=SAMPLE_SIZE).fit(XS)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    c_labels = db.labels_

    # number of clusters in labels, ignoring noise if present
    n_clusters = len(set(c_labels)) - (1 if -1 in c_labels else 0)
    n_noise = list(c_labels).count(-1)
    print(f'Estimated number of clusters: {n_clusters}')
    print(f'Estimated number of noise data points: {n_noise}')

    # plotting
    plt.scatter(x, y, c='indigo', marker='.', label='Original Data')
    plt.xlabel(r'$\mu_{\alpha*} cos(\delta)$' + ' (mas/yr)')
    plt.ylabel(r'$\mu_{\delta}$' + ' (mas/yr)')
    plt.title('Vector Point Diagram with DBSCAN selection')
    plt.scatter(x[c_labels == 0], y[c_labels == 0], marker='.', c='salmon', label='DBSCAN selection')
    plt.legend(loc='best')
    plt.show()

    # corresponding data extraction
    new_pmra = x[c_labels == 0]
    df = df[df['pmra'].isin(new_pmra)]
    df.to_csv('./csv/reduced.csv', index=False)

if __name__ == '__main__':
    main()
