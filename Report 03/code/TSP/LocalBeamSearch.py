import numpy as np

def local_beam_search(graph, k=10, max_iters=10000):
    TOTAL_SUM = 0
    for i in graph:
        for j in i:
            TOTAL_SUM += j
    def evaluate(state):
        return TOTAL_SUM - sum([graph[state[i - 1]][state[i]] for i in range(len(graph))])

    def neighbors(state):
        ret = []

        for i in range(len(graph) - 1):
            ret.append([*state[:i], state[i + 1], state[i], *state[i + 2:]])

        ret.append([state[-1], *state[1: -1], state[0]])

        return ret
    
    initials = []
    for i in range(k):
        nn = np.random.permutation(len(graph))
        val = evaluate(nn)
        initials.append((val, nn))

    states = initials

    for steps in range(max_iters):
        #  for state in states:
        #      if if_goal(state[1]):
        #          return state[1], steps
        new_states = []
        for state in states:
            mn = state
            for ns in neighbors(state[1]):
                val = evaluate(ns)
                nn = (val, ns)
                if mn[0] < nn[0]:
                    mn = nn
            new_states.append(mn)
        states = new_states[:k]

    new_states.sort(key=lambda x: x[0])
    return states[0][1], max_iters, states[0][0]
