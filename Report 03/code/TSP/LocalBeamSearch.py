from solutions.utils import *
import numpy as np

def LocalBeamSearch(graph, k=10):
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
    
    initials = []
    for i in range(k):
        new = np.random.permutation(len(graph))
        val = evaluate(new)
        initials.append((val, new))

    states = initials

    steps = 0
    while True:
        for state in states:
            if if_goal(state[1]):
                return state[1], steps
        new_states = [*states]
        for state in states:
            for ns in neighbors(state):
                val = evaluate(ns)
                np = (val, ns)
                if np in new_states:
                    continue
                new_states.append(np)
        new_states.sort(key=lambda x: x[0])
        states = new_states[:k]

        steps += 1
