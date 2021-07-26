#!/usr/bin/env python

'''
radius.py: Determines the optimal radius for the cluster

           The data grouped using sweeping distances from the mean centers. Each group has its
           Transition Parameter calculated, which is then used to esimate the radius of the cluster.
           The radius at which the Transition Parameter takes the largest value is considered to be
           covering radius for the cluster. The dataframe is converted to a new CSV for future use. 
'''

# imports
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import heapq as hq
from sklearn.linear_model import LinearRegression
from scipy.stats import gaussian_kde
from math import sqrt, atan, pi

__author__ = 'Rik Ghosh'
__copyright__ = 'Copyright 2021, The University of Texas at Austin'
__credits__ = ['Katherine Clark', 'Soham Saha', 'Mihir Suvarna']
__license__ = 'MIT'
__version__ = '1.5.4'
__maintainer__ = 'Rik Ghosh'
__email__ = 'rikghosh487@gmail.com'
__status__ = 'Production'

# globals
NT = r'$N_t$'

# assigns weight to each element in order to make a weighted graph data structure
def graph_weight(dataframe):
    graph = dict()
    pmra = np.array(dataframe['pmra'])
    pmdec = np.array(dataframe['pmdec'])
    ids = np.array(dataframe['source_id'])

    for i in range(len(dataframe)):
        for j in range(i + 1, len(dataframe)):
            # compute distance between two data points to store as edge weight
            deltax = abs(pmra[i] - pmra[j])
            deltay = abs(pmdec[i] - pmdec[j])
            weight = sqrt(deltax ** 2. + deltay ** 2.)
            if ids[i] not in graph:
                graph.setdefault(ids[i], {})
            graph.get(ids[i]).setdefault(ids[j], weight)
            if ids[j] not in graph:
                graph.setdefault(ids[j], {})
            graph.get(ids[j]).setdefault(ids[i], weight)
    return graph

# simulates minimum spanning tree from a weighted graph and a starting vertex and displays average edge length
def spanning_tree(graph, starting_vertex):
    visited = set([starting_vertex])  # assigns starting_vertex as visited
    edges = [(cost, starting_vertex, to) for to, cost in graph[starting_vertex].items()]
    hq.heapify(edges)  # uses heap queue for MST

    # initializing loop parameters
    count = curr_cost = 0
    avglen = [0]

    # graph loop for Prim's Algorithm
    while edges:
        cost, frm, to = hq.heappop(edges)
        # check for previously visited vertices to prevent cycles
        if to not in visited:
            curr_cost += cost
            count += 1
            avglen.append(curr_cost / count)  # computes average length of the MST per iteration
            visited.add(to)
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    hq.heappush(edges, (cost, to, to_next))
    
    x = np.linspace(0, len(graph) - 1, len(graph))  # x values for plotting
    normx = list(map(lambda c: c / max(x), x))  # x values normalized for plotting
    normlen = list(map(lambda c: c / max(avglen), avglen))   # y values normalized for plotting
    return (normx, normlen)

# determines the inclination angles of left-sided and right-sided lines of best fit to locate transition points
def inclination_angle(nmin, xvals, yvals):
    vals = list()
    cangle = list()
    fangle = list()
    model = LinearRegression()

    # span all possible points where Nmin < Nt < Ndat - Nmin
    for i in range(nmin, len(xvals) - nmin):
        # obtain all points for linear regression
        xleft = np.array(xvals[i - nmin:i + 1]).reshape(-1, 1)
        yleft = np.array(yvals[i - nmin:i + 1])
        xright = np.array(xvals[i:i + nmin + 1]).reshape(-1, 1)
        yright = np.array(yvals[i:i + nmin + 1])
        vals.append(i)

        # linear regression to find slope and compute angle of inclination
        model.fit(xleft, yleft)
        cangle.append(atan(model.coef_[0]) * 180 / pi)  # cluster angle
        model.fit(xright, yright)
        fangle.append(atan(model.coef_[0]) * 180 / pi)  # field angle
    
    return (vals, cangle, fangle)

# main function
def main():
    # constants
    FILENAME = r'./csv/vpd_adj.csv'
    MEAN_INDEX = 442
    MAX_RAD = 40

    # dataframe
    df = pd.read_csv(FILENAME)
    cent_ra = df['ra'][MEAN_INDEX]
    cent_dec = df['dec'][MEAN_INDEX]

    # adding distance to dataframe
    dist = list()
    for i in range(len(df)):
        dx = abs(df['ra'][i] - cent_ra)
        dy = abs(df['dec'][i] - cent_dec)
        dist.append(sqrt(dx ** 2. + dy ** 2.) * 60)
    df['dist'] = dist

    xrange = np.arange(0, MAX_RAD + 0.2, 0.2)   # x values for plot
    tparam = list() # initalizing y value container

    for elem in xrange:
        small = df[df['dist'] < elem]
        START_ID = 2013561830362788096
        gr = graph_weight(small)
        # calculate T parmater if data available
        if gr:
            normx, normlen = spanning_tree(gr, START_ID)
            ndat = len(normx)
            nmin = round(3 * sqrt(ndat))
            xvals, cluster, field = inclination_angle(nmin, normx, normlen)
            if cluster:
                ALPHA_MAX = 90
                DELTA = 0.01 * ALPHA_MAX
                transition = list()
                for i in range(len(cluster)):
                    diff = field[i] - cluster[i]
                    transition.append((diff / max(cluster[i], DELTA)) * (DELTA / ALPHA_MAX))
                tparam.append(max(transition))
            else:
                tparam.append(0)
        else:
            tparam.append(0)

    s = np.std(tparam)
    eta_max = max(tparam)
    plt.plot(xrange, tparam, label='Transition Parameter')
    plt.axhline(eta_max - 3 * s, color='r', linestyle='--', label='Selection Threshold')
    plt.legend(loc='best')
    plt.xlabel(r'$R_s$' + ' (arcmin)')
    plt.ylabel(r'$\eta_{max}$')
    plt.title('Transition Parameter per Cluster Radii')
    plt.show()

    print(f'Covering Radius: {xrange[tparam.index(eta_max)]}')

    df = df[df['dist'] < xrange[tparam.index(eta_max)]]
    df.to_csv('./csv/final.csv', index=False)

if __name__ == '__main__':
    main()
