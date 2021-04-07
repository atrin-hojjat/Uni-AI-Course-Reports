import numpy as np
import random

def local_beam_search(n, sat, k=10, max_iters=1000):
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
    
    initials = []
    for i in range(k):
        nn = [(random.random() < 0.5) for i in range(n)]
        val = evaluate(nn)
        initials.append((val, nn))

    states = initials

    for steps in range(max_iters):
        for state in states:
            if state[0] == len(sat):
                return state[1], steps, len(sat)
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
