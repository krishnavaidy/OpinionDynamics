"""
Program to implement Erdos Reyni graph or binomial graph for CS 886 with
networkx package

Krishna Vaidyanathan
"""
import networkx as nx
import random
import math
import csv

# Global variables

# learning factor
r = 1.5

# Size of graph
n = 200

# Init graph with values
def init_graph():
    # Initialize graph
    g = nx.binomial_graph(n, 0.02)

    # Opinions
    # Initialize initial opinion values
    # Extreme values
    for i in range(0, 20):
        g.node[i]['x'] = 1

    for i in range(180, n):
        g.node[i]['x'] = 0

    # Moderate values
    for i in range(20, 180):
        g.node[i]['x'] = random.random()%0.5

    # Empathy vanlues
    for i in range(0, n):
        g.node[i]['h'] = random.random()%0.01

    # Edge weights - uniform as of now due to paucity of time
    e = g.edges()
    weights  = {}
    for i in range(0, len(e)):
        weights[e[i]] = 1

    nx.set_edge_attributes(g, 'w', weights)
    for i in g.nodes():
        #g[g.node[i]][g.node[i]]['w'] = 1
        g.add_edge(i,i)
        e = nx.all_neighbors(g, i)
        l = 0
        for _ in e:
            l = l + 1

        g[i][i]['w'] = l

    return g

# Updates opinions and weights of graph g
def opinion_update(g):

    # Update opinions
    for i in g.nodes():
        Ni = nx.all_neighbors(g, i)
        # summation of neighbors
        weighted_opinion = 0
        weights = 0
        for j in Ni:
            weighted_opinion = weighted_opinion + g[i][j]['w']* g.node[j]['x']
            weights = weights + g[i][j]['w']

        g.node[i]['x'] = (g.node[i]['x'] * g[i][i]['w'] + weighted_opinion)/(g[i][i]['w'] + weights)

    # Update weights
    e = g.edges()
    for i in e:
        exp_value = math.pow((g.node[i[0]]['x'] - g.node[i[1]]['x']),2)
        T = math.exp(-exp_value/g.node[i[0]]['h'])
        g[i[0]][i[1]]['w'] = (g[i[0]][i[1]]['w'] + r*T)/(1 + r)



if __name__ == "__main__":
    # Number of iterations to avg opinion value over
    iterations = 25
    # Number of rounds for each iteration
    rounds = 500
    x_list = [0] * n
    h_list = [0] * n
    for i in range(0, iterations):
        g = init_graph()
        for j in range(0, rounds):
            opinion_update(g)
        nodes = g.nodes()
        for xi in nodes:
            x_list[xi] = x_list[xi] + g.node[xi]['x']
            h_list[xi] = h_list[xi] + g.node[xi]['h']

    x_list[:] = [x / (iterations) for x in x_list]
    h_list[:] = [h / (iterations) for h in h_list]
    # write to csv file
    wr_x = csv.writer(open("results.csv", 'wb'), dialect='excel')
    wr_h = csv.writer(open("h.csv", 'wv'), dialect='excel')
    for (i, j) in zip(x_list, h_list):
        wr_x.writerow([i])
        wr_h.writerow([j])
