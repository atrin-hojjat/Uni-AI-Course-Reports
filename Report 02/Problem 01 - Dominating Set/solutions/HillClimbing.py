from solutions.utils import *

def hill_climbing(graph, rand_start=0):
    def evaluate(state):
        ok, ls, lsd = is_goal(graph, state)
        return 2 * len(graph) - 2 * len(ls) - len(state)

    def neighbors(state):
        ret = []

        for i in range(len(graph)):
            if i in state:
                new = [*state]
                new.remove(i)
                ret.append(new)
            else:
                new = [*state, i]
                ret.append(new)
        return ret

    gen_start = []
    for i in range(len(graph)):
        if random.random() < rand_start:
            gen_start.append(i)
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
        steps = steps + 1
