import numpy as np
import random
import math

def genetic_algorithm(graph, max_iters=10000, fitness_threshold=0.01, population_size=10, p_mutation=0.05):
    TOTAL_SUM = 0
    for i in graph:
        for j in i:
            TOTAL_SUM += j
    def fitness(cell):
        return TOTAL_SUM - sum([graph[cell[i - 1]][cell[i]] for i in range(len(graph))])

    def mutate(cell):
        ind = random.randrange(len(graph))
        cell[ind], cell[ind - 1] = cell[ind - 1], cell[ind]

    def crossover(parent0, parent1):
        start, end = random.randrange(len(graph)), random.randrange(len(graph))
        if start > end:
            start, end = end, start
        child = [None] * len(graph)
        for i in range(start, end + 1):
            child[i] = parent0[i]
        ptr = 0
        for i in range(len(graph)):
            if child[i] == None:
                continue
            while parent1[ptr] in child:
                ptr += 1
            child[i] = parent1[ptr]
        return child


    def select_parents(population):
        #  tp = population.transpose()
        #  return np.random.choice(tp[1], 2, tp[0])
        return random.random.choice(
                [p[1] for p in population], k=2
                weights=[p[0] for p in population])

    initial_population = []
    for i in range(population_size):
        new = None
        while new is None or new in initial_population:
            new = np.random.permutation(len(graph))
        initial_population.append((fitness(new), new))
    population = initial_population

    best = initial_population(0)

    for i in range(max_iters):
        for i in population:
            if best[0] > i[0]:
                best = i
        new_pop = []

        for j in range(population_size):
            parents = select_parents(population)
            child = crossover(parents[0], parents[1])
            if random.random() < p_mutation:
                child = mutate(child)
            ft = fitness(child)
            new_pop.append((ft, child))
        population = new_pop

    return best[1], max_iters, best[0]
            
        


