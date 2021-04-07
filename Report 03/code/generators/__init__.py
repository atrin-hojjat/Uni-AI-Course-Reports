import random
import math

def gen_weighted_graph(nodes=20, wei_min=1, wei_max=100):

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
        for xi in range(-1, 2, 2):
            for j in range(i + 1):
                for xj in range(-1, 2, 2):
                    for k in range(j + 1):
                        for xk in range(-1, 2, 2):
                                if random.random() < p:
                                    clause = [xk * (k + 1), xj * (j + 1), xi * (i + 1)]
                                    sat.append(tuple(clause))

    return sat



