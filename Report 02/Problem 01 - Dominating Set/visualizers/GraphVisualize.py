import networkx as nx
import matplotlib
matplotlib.use("pgf")
import matplotlib.pyplot as plt
import os
import rich

def visualize_dominating_set(graph, dominating_set=[], name="",
        output=None):
    plt.figure()
    #  plt.title(name)
    G = nx.Graph()
    color_map = []
    for i in range(len(graph)):
        if i in dominating_set:
            color_map.append("#66CC99")
        elif len([j for j in graph[i] if j in dominating_set]):
            color_map.append("#112233")
        else:
            color_map.append("#FC575E")
    G.add_nodes_from([(i, ) for i in range(len(graph))])

    rich.print([(i, ) for i in range(len(graph))])
    rich.print(
            [
                (i, j, {"color": "#112233"}) 
                for i in range(len(graph)) for j in graph[i] if i < j
            ])
    G.add_edges_from(
            [
                (i, j, {"color": "#112233"}) 
                for i in range(len(graph)) for j in graph[i] if i < j
            ]
    )
    pos = nx.spring_layout(G, seed=10)
    nx.draw_networkx_edges(G, pos, alpha=0.2)
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=100)
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

