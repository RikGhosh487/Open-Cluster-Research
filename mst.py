# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import heapq as hq
from collections import defaultdict
from math import sqrt, atan, pi
from sklearn.linear_model import LinearRegression

# full scope constants
NT = r'$N_t$'

# assigns weight to each element in order to make a weighted graph data structure
def graph_weight(dataframe):
    graph = {}
    pmra = np.array(dataframe['pmra'])
    pmdec = np.array(dataframe['pmdec'])
    ids = np.array(dataframe['source_id'])

    for i in range(len(dataframe)):
        graph.setdefault(ids[i], {})
        for j in range(len(dataframe)):
            if i == j:
                continue
            if i > j:
                # using previously calculated cost for efficiency
                cost = graph.get(ids[j]).get(ids[i])
                graph.get(ids[i]).setdefault(ids[j], cost)
            else:
                # compute distance between two data points to store as edge weight
                deltax = abs(pmra[i] - pmra[j])
                deltay = abs(pmdec[i] - pmdec[j])
                weight = sqrt(deltax ** 2. + deltay ** 2.)
                graph.get(ids[i]).setdefault(ids[j], weight)
    return graph

# makes minimum spanning tree from a weighted graph and a starting vertex and displays if requested
def spanning_tree(graph, starting_vertex, display):
    mst = defaultdict(set)
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
            mst[frm].add(to)
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    hq.heappush(edges, (cost, to, to_next))
    
    x = np.linspace(0, len(graph) - 1, len(graph))  # x values for plotting
    
    # display graph if requested
    if(display):
        plt.plot(x, avglen, 'r--', label='Average length of MST edges per iteration')
        plt.xlabel(NT)
        plt.ylabel(r'$L_t$')
        plt.legend(loc='best')
        plt.title('Average Length of Edges of Spanning Tree per Iteration')
        plt.show()

    normx = list(map(lambda c: c / max(x), x))  # x values normalized for plotting
    normlen = list(map(lambda c: c / max(avglen), avglen))   # y values normalized for plotting
    return (mst, normx, normlen)

def inclination_angle(nmin, xvals, yvals):
    vals = []
    cangle = []
    fangle = []
    model = LinearRegression()

    # span all possible points where Nmin < Nt < Ndat - Nmin
    for i in range(nmin, len(xvals) - nmin):
        # obtain all points for linear regression
        xleft = np.array(xvals[i - nmin: i + 1]).reshape(-1, 1)
        yleft = np.array(yvals[i - nmin: i + 1])
        xright = np.array(xvals[i:i + nmin + 1]).reshape(-1, 1)
        yright = np.array(yvals[i:i + nmin + 1])
        vals.append(i)

        # linear regression to find slope and compute angle of inclination
        model.fit(xleft, yleft)
        cangle.append(atan(model.coef_[0]) * 180 / pi)  # cluster angle
        model.fit(xright, yright)
        fangle.append(atan(model.coef_[0]) * 180 / pi)  # field angle
    
    return (vals, cangle, fangle)

def main():
    # reading datafile and dropping missing fields
    df = pd.read_csv('results.csv')

    # statistical data reductions
    df = df[df['pmra_error'] < 1]
    df = df[df['pmdec_error'] < 1]

    # GAIA parallax correction
    df = df[df['parallax'] >= 0]

    # mst generation
    START_ID = 1189357258367438464  # source_id of data point closest to mean PMRA and mean PMDEC
    gr = graph_weight(df)   # get weighted graph
    _, normx, normlen = spanning_tree(gr, START_ID, True)

    # Nmin
    ndat = len(normx)
    nmin = round(3 * sqrt(ndat))
    xvals, cluster, field = inclination_angle(nmin, normx, normlen)

    # Inclination Plot
    plt.plot(xvals, cluster, 'b-', label=r'Cluster Angle $\alpha_c$')
    plt.plot(xvals, field, 'r--', label=r'Field Angle $\alpha_f$')
    plt.plot(xvals, np.zeros_like(xvals), 'c--')
    plt.xlabel(NT)
    plt.ylabel(r'$\alpha$ (deg)')
    plt.legend(loc='best')
    plt.title('Inclination Angle of Cluster and Field data per Iteration')
    plt.show()

    # Dimensionless Transition Parameter
    ALPHA_MAX = 90
    DELTA = 0.01 * ALPHA_MAX
    transition = []

    # calculate transition parameter at each point
    for i in range(len(cluster)):
        diff = field[i] - cluster[i]
        transition.append((diff / max(cluster[i], DELTA)) * (DELTA / ALPHA_MAX))

    plt.plot(xvals, transition, 'r-', label=r'Transition Parameter Value')
    plt.plot(xvals, np.zeros_like(xvals), 'b--')
    plt.xlabel(NT)
    plt.ylabel(r'$\eta$')
    plt.legend(loc='best')
    plt.title('Transition Paramater Graph')
    plt.show()

if __name__ == '__main__':
    main()