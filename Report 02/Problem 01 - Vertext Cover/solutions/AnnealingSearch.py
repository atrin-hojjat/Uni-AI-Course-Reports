from solutions.utils import * 

def annealing_search(graph, rand_start=0, 
        initial_temprature=1,
        schedule=lambda T, t: T * 0.98, 
        min_temprature=0.000001):
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

        t = t + 1
        T = schedule(T, t)
