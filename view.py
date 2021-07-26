#!/usr/bin/env python

'''
view.py: View the histograms and scatterplots for the data in the CSV

         A dataframe is created from the CSV and the parameters are displayed through histograms
         and scatterplots
'''

# imports
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull
from scipy.stats import gaussian_kde, norm

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
    FILENAME = r'./csv/final.csv'
    BINS = 50
    HIST_Y_LABEL = 'Count'
    CURVE_LABEL = 'Gaussian Fit'

    # dataframe
    df = pd.read_csv(FILENAME)

    '''HISTOGRAMS'''
    # ra
    x = np.array(df['ra'])
    hist, bins, _ = plt.hist(x, BINS, histtype='step', label='Counts')  # generate plot
    m = np.mean(x)
    s = np.std(x)
    p = norm.pdf(bins, m, s) # generate pdf
    plt.plot(bins, p / p.sum() * len(df), 'r--', label=CURVE_LABEL)
    plt.axvline(m, color='k', linestyle='-.', label='Mean')
    plt.xlabel(r'$\alpha$ (deg)')
    plt.ylabel(HIST_Y_LABEL)
    plt.legend(loc='best')
    plt.title(r'Right Ascension ($\alpha$) Histogram')
    plt.show()

    # dec
    x = np.array(df['dec'])
    hist, bins, _ = plt.hist(x, BINS, histtype='step', label='Counts')  # generate plot
    m = np.mean(x)
    s = np.std(x)
    p = norm.pdf(bins, m, s) # generate pdf
    plt.plot(bins, p / p.sum() * len(df), 'r--', label=CURVE_LABEL)
    plt.axvline(m, color='k', linestyle='-.', label='Mean')
    plt.xlabel(r'$\delta$ (deg)')
    plt.ylabel(HIST_Y_LABEL)
    plt.legend(loc='best')
    plt.title(r'Declination ($\delta$) Histogram')
    plt.show()

    # pmra
    x = np.array(df['pmra'])
    hist, bins, _ = plt.hist(x, BINS, histtype='step', label=CURVE_LABEL)  # generate plot
    m = np.mean(x)
    s = np.std(x)
    p = norm.pdf(bins, m, s) # generate pdf
    plt.plot(bins, p / p.sum() * len(df), 'r--', label=CURVE_LABEL)
    plt.axvline(m, color='k', linestyle='-.', label='Mean')
    plt.xlabel(r'$\mu_{\alpha} cos(\delta)$ (mas/yr)')
    plt.ylabel(HIST_Y_LABEL)
    plt.legend(loc='best')
    plt.title(r'Proper Motion in Right Ascension ($\mu_{\alpha*}$) Histogram')
    plt.show()

    # pmdec
    x = np.array(df['pmdec'])
    hist, bins, _ = plt.hist(x, BINS, histtype='step', label='Counts')  # generate plot
    m = np.mean(x)
    s = np.std(x)
    p = norm.pdf(bins, m, s) # generate pdf
    plt.plot(bins, p / p.sum() * len(df), 'r--', label=CURVE_LABEL)
    plt.axvline(m, color='k', linestyle='-.', label='Mean')
    plt.xlabel(r'$\mu_{\delta}$ (mas/yr)')
    plt.ylabel(HIST_Y_LABEL)
    plt.legend(loc='best')
    plt.title(r'Proper Motion in Declination ($\mu_{\delta}$) Histogram')
    plt.show()

    # parallax
    x = np.array(df['parallax'])
    hist, bins, _ = plt.hist(x, BINS, histtype='step', label='Counts')  # generate plot
    m = np.mean(x)
    s = np.std(x)
    p = norm.pdf(bins, m, s)
    plt.plot(bins, p / p.sum() * len(df), 'r--', label=CURVE_LABEL)
    plt.axvline(m, color='k', linestyle='-.', label='Mean')
    plt.xlabel(r'$\pi$ (mas)')
    plt.ylabel(HIST_Y_LABEL)
    plt.legend(loc='best')
    plt.title(r'Parallax ($\pi$) Histogram')
    plt.show()

    # correlation
    plt.hist(df['pmra_pmdec_corr'], BINS, histtype='step', label='Pmra Pmdec')
    plt.hist(df['parallax_pmra_corr'], BINS, histtype='step', label='Parallax Pmra')
    plt.hist(df['parallax_pmdec_corr'], BINS, histtype='step', label='Parallax Pmdec')
    plt.xlabel('Correlation')
    plt.ylabel(HIST_Y_LABEL)
    plt.legend(loc='best')
    plt.title('Correlation Coefficients')
    plt.show()

    '''SCATTERPLOTS'''
    # spatial position
    x = np.array(df['ra'])
    y = np.array(df['dec'])
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)
    plt.scatter(x, y, c=z, marker='.') # plotting
    plt.plot(np.mean(x), np.mean(y), 'r*', label='Mean')
    plt.xlabel(r'$\alpha$ (deg)')
    plt.ylabel(r'$\delta$ (deg)')
    plt.legend(loc='best')
    plt.title('Spatial Structure in ICRS')
    plt.show()

    # vpd
    x = np.array(df['pmra'])
    y = np.array(df['pmdec'])
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)
    s = xy.T
    hull = ConvexHull(s)
    plt.scatter(x, y, c=z, marker='.') # plotting
    plt.plot(np.mean(x), np.mean(y), 'r*', label='Mean')
    plt.xlabel(r'$\mu_{alpha} cos(\delta)$ (mas/yr)')
    plt.ylabel(r'$\mu_{delta}$ (mas/yr)')
    for simplex in hull.simplices:
        plt.plot(s[simplex, 0], s[simplex, 1], 'k-')
    plt.legend(loc='best')
    plt.title('Vector Point Diagram')
    plt.show()

    # cmd
    x = np.array(df['bp_rp'])
    y = np.array(df['phot_g_mean_mag'])
    plt.gca().invert_yaxis()
    plt.scatter(x, y, marker='.', label='Datapoint')
    plt.xlabel(r'$B_P - R_P$ (mag)')
    plt.ylabel(r'$G$ (mag)')
    plt.legend(loc='best')
    plt.title('Color Magnitude Diagram')
    plt.show()

if __name__ == '__main__':
    main()
