import math
import heapq
import random

def is_goal(graph, state):
    ls = {}
    for i in range(len(graph)):
        ls[i] = ""
    for v in state:
        if v in ls:
            del ls[v]
        for u in graph[v]:
            if u in ls:
                del ls[u]
    return len(ls) == 0, [*ls.keys()], ls
