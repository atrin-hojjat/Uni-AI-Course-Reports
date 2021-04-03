import numpy as np
import random
import math

def genetic_algorithm(n, sat, max_iters=10000, fitness_threshold=0.01, population_size=10, p_mutation=0.05):
    def fitness(state):
        cnt = 0
        for i in sat:
            for t in state:
                if state[t] == 1:
                    cnt += 1
                    break
        return cnt

    def mutate(cell):
        ncell = list(cell)
        i = random.randrange(len(n))
        ncell[i] = not ncell[i]
        return ncell

    def crossover(parent0, parent1):
        start, end = random.randrange(len(n)), random.randrange(len(n))
        if start > end:
            start, end = end, start
        child = [None] * len(n)
        for i in range(start, end + 1):
            child[i] = parent0[i]
        ptr = 0
        for i in range(start):
            child[i] = parent1[ptr]
        for i in range(end + 1, n):
            child[i] = parent1[ptr]
        return child


    def select_parents(population):
        #  tp = population.transpose()
        #  return np.random.choice(tp[1], 2, tp[0])
        return random.choices(
                [p[1] for p in population], k=2,
                weights=[p[0] for p in population])

    initial_population = []
    for i in range(population_size):
        new = None
        while new is None or new in initial_population:
            new = list(np.random.permutation(len(n)))
        initial_population.append((fitness(new), new))
    population = initial_population

    best = initial_population[0]

    for i in range(max_iters):
        for i in population:
            if best[0] < i[0]:
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
    for i in population:
        if best[0] < i[0]:
            best = i

    return best[1], max_iters, best[0]
            
        


