import numpy as np
import random

def hill_climbing(n, sat, rand_start=0):
    def evaluate(state):
        cnt = 0
        for i in sat:
            for t in state:
                if state[t] == 1:
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

    steps = 0
    while True:
        selected_neighbor = state

        for neighbor in neighbors(state[1]):
            val = evaluate(neighbor)
            if val > selected_neighbor[0]:
                selected_neighbor = (val, neighbor)

            if selected_neighbor[1] == state[1]:
                return state[1], steps, state[0]

            state = selected_neighbor
            steps += 1

