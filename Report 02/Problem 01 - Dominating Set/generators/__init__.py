import random

def gen_graph_eq_prob_edges(nodes=100, p=0.1):
    """
    Generates a graph with $nodes vertices where each edge has a $p probibility of existing. 
    The graph is represented by a list of vertices each represented as a list of vertices it's connected to.
    O(nodes ^ 2)
    """
    graph = [[] for i in range(nodes)]

    for i in range(nodes):
        for j in range(i):
            if random.random() < p:
                graph[i].append(j)
                graph[j].append(i)
    return graph

def gen_graph_fix_set_edges(nodes=100, edges=900):
    """
    Generates a graph with $nodes vertices and $edges edges
    The graph is represented by a list of vertices each represented as a list of vertices it's connected to.
    O(nodes ^ 2)
    """
    graph = [[] for i in range(nodes)]

    all_edges = []
    
    for i in range(nodes):
        for j in range(i):
            all_edges.append((i, j, ))

    for i in range(edges):
        x = random.randrange(0, len(all_edges))
        edge = all_edges[x]
        graph[edge[0]].append(edge[1])
        graph[edge[1]].append(edge[0])
        all_edges.pop(x)

    return graph



