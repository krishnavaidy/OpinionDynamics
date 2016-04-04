"""
Program to implement Caveman graph for CS 886 with networkx package

Krishna Vaidyanathan
"""
import networkx as nx
import random
import math
import csv
import Image

# Global variables

# learning factor
r = 1.5

# Size of graph
n = 200

# Number of cliques
nc = 5

# Step
step = int(n/nc)

# h value
h = 1

# weight matrix
w = [[0] * n]*n

# Init graph with values
def init_graph():
    # Initialize graph
    # g = nx.binomial_graph(n, p, seed=None, directed=False)
    g = nx.Graph()
    
    # Add n nodes
    for i in range(0, n):
        g.add_node(i)

    # Add edges
    # Add clique edges
    for i in range(step, n, step):
        for j in range(i - step, i):
            for k in range(i-step, i):
                g.add_edge(i,j)
                g.add_edge(j,i)

    # Add edges between cliques
    for i in range(step, n, step):
        g.add_edge(i - 5, i + 3)

    # Opinions
    # Initialize initial opinion values
    for j in range(0, n, step):
        # Extreme values
        for i in range(j, int(j + step * 1/10)):
            g.node[i]['x'] = 1

        for i in range(int(j + step*9/10),j + step):
            g.node[i]['x'] = 0

        # Moderate values
        for i in range(int(j + step*1/10),int(j + step*9/10)):
            g.node[i]['x'] = random.random()%0.5

    # Empathy values
    for i in range(0, n):
        g.node[i]['h'] = random.gauss(0.5, 0.01)

    # Curmudegeons 
    for i in range(0, n):
        g.node[i]['c'] = False

    # for i in range(10, 50):
        # g.node[i]['c'] = True

    # Edge weights - uniform as of now due to paucity of time
    e = g.edges()
    weights  = {}
    for i in range(0, len(e)):
        # Set weight to 0 if node is a curmudegeon
        if g.node[e[i][0]] == True:
            weights[e[i]] = 0
        else:
            weights[e[i]] = 1

        w[e[i][0]][e[i][1]] = 1
        w[e[i][1]][e[i][0]] = 1

    nx.set_edge_attributes(g, 'w', weights)
    for i in g.nodes():
        #g[g.node[i]][g.node[i]]['w'] = 1
        g.add_edge(i,i)
        e = nx.all_neighbors(g, i)
        l = 0
        for _ in e:
            l = l + 1

        g[i][i]['w'] = l
        w[i][i] = l


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
            weighted_opinion = weighted_opinion + w[i][j]* g.node[j]['x']
            weights = weights + w[i][j]

        # Only update opinion if not a curmudgeon
        if(g.node[i]['c'] == False):
            g.node[i]['x'] = (g.node[i]['x'] * w[i][i] + 
                    weighted_opinion)/(w[i][i] + weights)

    # Update weights
    e = g.edges()
    for i in e:
        exp_value = math.pow((g.node[i[0]]['x'] - g.node[i[1]]['x']),2)
        T = math.exp(-exp_value/g.node[i[0]]['h'])
        w[i[0]][i[1]] = (w[i[0]][i[1]] + r*T)/(1 + r)
        # If a curmudegeon then weight is always 0
        if(g.node[i[0]]['c'] == True):
            w[i[0]][i[1]] = 0 



def main(result_file):
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
    wr_x = csv.writer(open(result_file + '.csv', 'wb'), dialect='excel')
    wr_h = csv.writer(open("h.csv", 'wv'), dialect='excel')
    for (i, j) in zip(x_list, h_list):
        wr_x.writerow([i])
        wr_h.writerow([j])

    # Display polarization
    img = Image.new('L', (10, 20), "black")
    pixels = img.load()
    pixel_index = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            OldValue = (x_list[pixel_index])
            NewValue = (((OldValue - 0) * (255 - 0)) / (1 - 0)) + 0
            img.putpixel((i,j), NewValue)
    #img.show()
    img.save(result_file + '.png')

if __name__ == "__main__":
    # for h in range(1, 11, 1):
        # h = h/100.0
    main('polarization' + str(h))
