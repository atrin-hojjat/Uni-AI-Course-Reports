import networkx as nx
import matplotlib.pyplot as plt

def visualize_vertex_cover(graph, vertex_cover=[]):
    G = nx.Graph()
    color_map = []
    for i in range(len(graph)):
        if i in vertex_cover:
            color_map.append("#66CC99")
        elif len([j for j in graph[i] if j in vertex_cover]):
            color_map.append("#112233")
        else:
            color_map.append("#FC575E")
    G.add_nodes_from([(i, {"color": "red" if i in vertex_cover else
        "blue"}) for i in range(len(graph))])

    G.add_edges_from(
            [
                (i, j, {"color": "#112233"}) 
                for i in range(len(graph)) for j in graph[i] if i < j
            ]
    )
    pos = nx.spring_layout(G)
    nx.draw_networkx_edges(G, pos, alpha=0.2)
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=100)
    plt.show()

