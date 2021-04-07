import numpy as np
import random
import math

def annealing_search(n, sat, rand_start=1, initial_temprature=1,
        schedule=lambda T, t: T * 0.98,
        min_temprature=0.000001):
    def evaluate(state):
        cnt = 0
        for i in sat:
            for t in i:
                if t > 0 and state[t - 1] == 1:
                    cnt += 1
                    break
                elif t < 0 and state[-t - 1] == 0:
                    cnt += 1
                    break
        return cnt

    def neighbors(state):
        ret = []

        for i in range(n):
            nn = [*state]
            nn[i] = not nn[i]
            ret.append(nn)

        return ret
    
    gen_start = [False for i in range(n)]
    if rand_start == 1:
        gen_start = [(random.random() < 0.5) for i in range(n)]

    state = (evaluate(gen_start), gen_start)

    pcurn = None

    t, T = 1, initial_temprature
    while True:
        if T < min_temprature:
            return state[1], t, state[0]
        cur_neighbors = pcurn if pcurn is not None else neighbors(state[1])
        nxid = random.randrange(0, len(cur_neighbors))
        nxt = cur_neighbors[nxid]
        nxt_val = evaluate(nxt)

        deltE = nxt_val - state[0]

        if deltE > 0 or random.random() < math.e ** (deltE / T):
            state = (nxt_val, nxt)

        t += 1
        T = schedule(T, t)
