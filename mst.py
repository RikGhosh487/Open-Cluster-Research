#!/usr/bin/env python

'''
mst.py: Takes a CSV file and computes the minimum spanning tree with the Vector Point Diagram (VPD) to find the
        members of the cluster and determine the limiting radius.

        The algorithm takes a data frame and assigns a weight (determined by the distance from one data point to the other in the VPD) to each data point in the data frame. Then Prim's algorithm is used to make a
        minimum spanning tree (MST) from a starting vertex that is relatively close to the mean PMRA and PMDEC
        values. The average length of each of the edges per iteration is computed and used to find a transition
        point that indicates the edge of the cluster, and thus a cluster separation from the field stars
'''

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import heapq as hq
from collections import defaultdict
from math import sqrt, atan, pi
from sklearn.linear_model import LinearRegression

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
def spanning_tree(graph, starting_vertex, display, mins=0):
    visited = set([starting_vertex])  # assigns starting_vertex as visited
    edges = [(cost, starting_vertex, to) for to, cost in graph[starting_vertex].items()]
    hq.heapify(edges)  # uses heap queue for MST

    # initializing loop parameters
    count = curr_cost = 0
    avglen = [0]
    mems = [starting_vertex]

    # graph loop for Prim's Algorithm
    while edges:
        cost, frm, to = hq.heappop(edges)
        # check for previously visited vertices to prevent cycles
        if to not in visited:
            if count < mins:
                mems.append(to)
            curr_cost += cost
            count += 1
            avglen.append(curr_cost / count)  # computes average length of the MST per iteration
            visited.add(to)
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    hq.heappush(edges, (cost, to, to_next))
    
    x = np.linspace(0, len(graph) - 1, len(graph))  # x values for plotting
    
    # display graph if requested
    if(display):
        plt.plot(x, avglen, 'r--', label='Average length of MST edges per Iteration')
        plt.xlabel(NT)
        plt.ylabel(r'$L_t$')
        plt.legend(loc='best')
        plt.title('Average Length of Edges of Spanning Tree per Iteration')
        plt.show()

    normx = list(map(lambda c: c / max(x), x))  # x values normalized for plotting
    normlen = list(map(lambda c: c / max(avglen), avglen))   # y values normalized for plotting
    return (normx, normlen, mems)

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
    FILENAME = './csv/stat_adj.csv'

    # dataframe
    df = pd.read_csv(FILENAME)

    # mst generation
    START_ID = 2013610376379103104  # source_id of data point closest to mean PMRA and mean PMDEC
    gr = graph_weight(df)  # get weighted graph
    normx, normlen, _ = spanning_tree(gr, START_ID, True)

    # Nmin
    ndat = len(normx)
    nmin = round(3 * sqrt(ndat))
    xvals, cluster, field = inclination_angle(nmin, normx, normlen)

    # Inclination Plot
    plt.plot(xvals, cluster, 'b-', label=r'Cluster Angle ($\alpha_c$)')
    plt.plot(xvals, field, 'r--', label=r'Field Angle ($\alpha_f$)')
    plt.plot(xvals, np.zeros_like(xvals), 'c--')
    plt.xlabel(NT)
    plt.ylabel(r'$\alpha$ (deg)')
    plt.legend(loc='best')
    plt.title('Inclination Angle of Cluster and Field data per Iteration')
    plt.show()

    # Dimensionless Transition Parameter
    ALPHA_MAX = 90
    DELTA = 0.01 * ALPHA_MAX
    transition = list()

    # calculate transition parameter at each point
    for i in range(len(cluster)):
        diff = field[i] - cluster[i]
        transition.append((diff / max(cluster[i], DELTA)) * (DELTA / ALPHA_MAX))

    index = transition.index(max(transition))
    xmax = xvals[index]

    # plotting
    plt.plot(xvals, transition, 'r-', label='Transition Parameter Value')
    plt.plot(xvals, np.zeros_like(xvals), 'b--')
    plt.plot(xmax, transition[index], 'x', label='Transition Point')
    plt.xlabel(NT)
    plt.ylabel(r'$\eta$')
    plt.legend(loc='best')
    plt.title('Transition Paramater Graph')
    plt.show()

    _, _, mems = spanning_tree(gr, START_ID, False, xmax)
    data = pd.read_csv(FILENAME, index_col='source_id')
    bprp = list()
    g = list()
    for elem in mems:
        bprp.append(data.loc[elem]['bp_rp'])
        g.append(data.loc[elem]['phot_g_mean_mag'])

    plt.plot(df['bp_rp'], df['phot_g_mean_mag'], 'b.', label='Original Data')
    plt.plot(bprp, g, 'r.', label='MST Data')
    plt.xlabel(r'$B_P-R_P$' + ' (mag)')
    plt.gca().invert_yaxis()
    plt.ylabel(r'$G$' + ' (mag)')
    plt.legend(loc='best')
    plt.show()

    df2 = df[df['source_id'].isin(mems)]
    df2.to_csv('./csv/vpd_adj.csv', index=False)

if __name__ == '__main__':
    main()
