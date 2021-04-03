from solutions.utils import *
import numpy as np

def hill_climbing(graph, rand_start=0):
    TOTAL_SUM = 0
    for i in graph:
        for j in i:
            TOTAL_SUM += j
    def evaluate(state):
        return TOTAL_SUM - sum([graph[cell[i - 1]][cell[i]] for i in range(len(graph))])

    def neighbors(state):
        ret = []

        for i in range(len(graph)):
            ret.append([*state[:i], state[i + 1], state[i], *state[i + 2:]])

        ret.append([state[-1], *state[1: -1], state[0]])

        return ret
    
    gen_start = range(len(graph))
    if rand_start == 1:
        gen_start = np.random.permutation(len(graph)) - 1

    state = (evaluate(gen_start), gen_start)

    steps = 0
    while True:
        selected_neighbor = state

        for neighbor in neighbors(state[1]):
            val = evaluate(neighbor)
            if val > selected_neighbor[0]:
                selected_neighbor = (val, neighbor)

            if selected_neighbor[1] == state[1]:
                return state[1], steps

            state = selected_neighbor
            steps += 1

