"""
Program to implement Erdos Reyni graph or binomial graph for CS 886 with
networkx package

Krishna Vaidyanathan
"""
import networkx as nx
import random
import math

# learning factor
r = 1.5

# Size of graph
n = 200
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
    g.node[i]['x'] = 0.5

# Empathy values
for i in range(0, n):
    g.node[i]['h'] = random.random()%0.1

# Edge weights - uniform as of now due to paucity of time
e = g.edges()
weights  = {}
for i in range(0, len(e)):
    weights[e[i]] = 1

nx.set_edge_attributes(g, 'w', weights)
for i in g.nodes():
    #g[g.node[i]][g.node[i]]['w'] = 1
    g.add_edge(i,i)
    g[i][i]['w'] = 1

# Rounds
def opinion_update():

    # Update opinions
    for i in g.nodes():
        Ni = nx.all_neighbors(g, i)
        # summation of neighbors
        weighted_opinion = 0
        weights = 0
        for j in Ni:
            weighted_opinion = weighted_opinion + g[i][j]['w']* g.node[j]['x']
            weights = weights + g[i][j]['w']

        g.node[i]['x'] = (g.node[i]['x'] * g[i][i]['w'] + weighted_opinion)/(g[i][i]['w'] + weighted_opinion)

    # Update weights
    e = g.edges()
    for i in e:
        exp_value = math.pow((g.node[i[0]]['x'] - g.node[i[1]]['x']),2)
        T = math.exp(exp_value/g.node[i[0]]['h'])
        g[i[0]][i[1]]['w'] = (g[i[0]][i[0]]['w'] + r*T)/(1 + r)



opinion_update()


