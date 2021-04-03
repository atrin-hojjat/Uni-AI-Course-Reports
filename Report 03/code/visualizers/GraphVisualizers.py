import networkx as nx
import matplotlib
#  matplotlib.use("pgf")
import matplotlib.pyplot as plt
import os
import rich

def visualize_tsp(graph, path=[], name="",
        output=None):
    plt.figure()
    plt.title(name)
    G = nx.Graph()
    color_map = []
    for i in range(len(graph)):
        if i in path:
            color_map.append("#66CC99")
        else:
            color_map.append("#112233")
    G.add_nodes_from([i for i in range(len(graph))])
    path_edges = [sorted((path[i - 1], path[i])) for i in range(len(path))]
    print(path)
    print(graph)
    print(path_edges)
    G.add_edges_from(
            [
                (i, j, {'weight':  graph[i][j], 
                    'color': '#112233' if (i, j) not in path_edges else '#FC575E'})
                for i in range(len(graph)) for j in range(len(graph[i])) if (i < j)
            ]
    )
    G.add_edge(2, 5, weight=3)
    for i in range(len(path)):
        G.edges[path[i - 1], path[i]]['color'] = 'red'
    #  G.add_edges_from(
    #          [
    #              (path[i - 1], path[i], {'weight': graph[path[i - 1]][path[i]]})
    #              for i in range(len(path))

    #          ],
    #          color="#FC575E"
    #  )
    pos = nx.shell_layout(G)
    edge_colors = nx.get_edge_attributes(G,'color').values()
    nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color=edge_colors)
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=100)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    if output:
        if not os.path.exists(os.path.dirname(os.path.join("./output", output, f"{name}.jpg"))):
            try: os.makedirs(os.path.dirname(os.path.join("./output", output, f"{name}.jpg")))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        plt.savefig(os.path.join("./output", output, f"{name}.jpg"))
        matplotlib.rcParams.update({
            "pgf.texsystem": "pdflatex",
            'font.family': 'mononoki Nerd Font Mono',
            'text.usetex': True,
            'pgf.rcfonts': False,
        })
        plt.savefig(os.path.join("./output", output, f"{name}.pgf"))
    plt.show()

