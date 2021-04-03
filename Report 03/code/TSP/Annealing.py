from solutions.utils import *
import numpy as np

def annealing_search(graph, rand_start=0, initial_temprature=1,
        schedule=lambda T, t: T * 0.98,
        min_temprature=0.000001):
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

    pcurn = None

    t, T = 1, initial_temprature
    while True:
        if T < min_temprature:
            return state[1], t
        cur_neighbors = pcurn if pcurn is not None else neighbors(state[1])
        nxid = random.randrange(0, len(cur_neighbors))
        nxt = cur_neighbors[nxid]
        nxt_val = evaluate(nxt)

        deltE = nxt_val - state[0]

        if deltE > 0 or random.random() < math.e ** (deltE / T):
            state = (nxt_val, nxt)

        t += 1
        T = schedule(T, t)
