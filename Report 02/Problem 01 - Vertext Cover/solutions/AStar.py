from solutions.utils import *

def Astar(graph):
    n = len(graph)

    states = [(0, [])]

    def h(state):
        ok, ls, lsd = is_goal(graph, state)
        if ok:
            return 0
        mx = 0
        for i in ls:
            deg = 0
            for j in graph[i]:
                if j in lsd:
                    deg = deg + 1
            mx = max(mx, deg + 1)
        return len(ls) / mx


    def f(state):
        return h(state) + len(state)
    steps = 0
    while True:
        cost, cur = heapq.heappop(states)
        print(cost, cost - len(cur), cur)
        if is_goal(graph, cur)[0]:
            return cur, steps

        for i in range(cur[-1] + 1 if len(cur) else 0, n):
            if i not in cur:
                new_state = [*cur, i]
                heapq.heappush(states, (f(new_state), new_state))
        steps = steps + 1
    return []
