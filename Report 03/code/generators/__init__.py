import random
import math

def gen_weighted_graph(nodes=30, wei_min=0, wei_max=100):

    graph = [[0 for j in range(nodes)] for i in range(nodes)]

    for i in range(nodes):
        for j in range(i):
            wei = math.floor(random.random() * (wei_max - wei_min)) + wei_min
            graph[i][j] = wei
            graph[j][i] = wei
    return graph

def gen_sat(variables=20, p=0.2):
    sat = []
    
    for i in range(variables):
        for j in range(i + 1):
            for k in range(j + 1):
                if random.random() < p:
                    sat.append((k, j, i))

    return sat



