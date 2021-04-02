import networkx as nx
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import matplotlib
matplotlib.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import os
import numpy as np
import rich


def SetupLibraries():
    matplotlib.rcParams.update({
        "pgf.texsystem": "xelatex",
        'text.usetex': True,
        'pgf.rcfonts': False,
        "font.family": "mononoki Nerd Font Mono",
        "font.serif": [],
        #  "font.cursive": ["mononoki Nerd Font", "mononoki Nerd Font Mono"],
    })


def plot_data(testname, x_lab, y_lab, ls, output=None):
    plt.figure()
    plt.title(testname)
    colors = ["#112233", "#66CC99", "#44BBFF", "#FC575E", "#c955f7"]
    rich.print(ls)
    for x in range(len(ls)):
        val = ls[x]
        plt.plot(val['X'], val['Y'], colors[x], label=val['name'],
                linewidth=1)
        print(x, val)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.legend()
    if output:
        if not os.path.exists(os.path.dirname(os.path.join("./output",
            output, f"{testname}.jpg"))):
            try: os.makedirs(os.path.dirname(os.path.join("./output",
                output, f"{testname}.jpg")))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        plt.savefig(os.path.join("./output", output, f"{testname}.jpg"))
        plt.savefig(os.path.join("./output", output, f"{testname}.pgf"))
    plt.show()


def plot_stacked_bar(testname, x_lab, y_lab, ls, output=None):
    plt.figure()
    plt.title(testname)
    colors = [["#112233", "#3973ac", "#9fbfdf", "#ecf2f9"], 
            ["#3aaf75", "#66CC99", "#8fdab5", "#effaf4"], 
            ["#00a2ff", "#44BBFF", "#9ddbff", "#ebf8ff"], 
            ["#d4040d", "#FC575E", "#fd9fa3", "#ffeced"], 
            ["#7b08a9", "#c955f7", "#e1a1fb", "#f9ecfe"]]


    rich.print(ls)
    #  width = 0.002
    width = (ls[0]['X'][1] - ls[0]['X'][0]) / (len(ls) + 2)
    legend_handles = []
    hndls = [[], [], [], []]

    for x in range(len(ls)):
        val = ls[x]
        prv = None
        legend_handles.append(mlines.Line2D([0], [0], color=colors[x][1], lw=4,
            label=val['name']))
        for j in range(len(val['Y'])):
            yl = val['Y'][j]
            p = plt.bar(np.array(val['X']) + width * (x - len(ls) / 2), yl, 
                    bottom=prv, width=width,
                    color=colors[x][j])
            hndls[j].append(p)

            if prv is not None:
                prv = prv + np.array(yl)
            else:
                prv = np.array(yl)

    names = []
    for j in range(len(colors[0])):
        names.append(f"Δ {'=' if j < 3 else '>='} {j}")
        hndls[j] = tuple(hndls[j])
        #  legend_handles.append(mlines.Line2D(hndls[j], [f"{Δ {'=' if j < 3 else '>='} {j}"],
        #      label=f"Δ {'=' if j < 3 else '>='} {j}"))

    plt.xlabel(x_lab)
    plt.ylabel(y_lab)

    #  plt.legend(hndls,
    #      names, loc='lower left', mode='expand',
    #          borderaxespad=0., bbox_to_anchor=(0., 1.02, 1., .102), ncol=2,
    #          handler_map={tuple: HandlerTuple(ndivide=None)})

    plt.legend(handles=legend_handles)

    #  for i in range(len(ls)):
    #  mpl_colors = matplotlib.colors.ListedColormap(colors[i])
    ncls = []
    for i in range(len(colors[0])):
        for j in range(len(ls)):
            ncls.append(colors[j][i])
    mpl_colors = matplotlib.colors.ListedColormap(ncls)
    bounds = np.arange(0, 4.00001, 1 / len(ls))
    norm = matplotlib.colors.BoundaryNorm(bounds, mpl_colors.N)

    cb1 = plt.colorbar(
        matplotlib.cm.ScalarMappable(cmap=mpl_colors, norm=norm),
        boundaries=bounds,  # Adding values for extensions.
        ticks=range(5),
        spacing='proportional',
        orientation='vertical',
        label='No. Nodes more than the best answer',
        aspect=40,

    )
    #  cb1.ax.yaxis.set_tick_params(pad=-10)


    if output:
        if not os.path.exists(os.path.dirname(os.path.join("./output",
            output, f"{testname}.jpg"))):
            try: os.makedirs(os.path.dirname(os.path.join("./output",
                output, f"{testname}.jpg")))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        plt.savefig(os.path.join("./output", output, f"{testname}.jpg"))
        matplotlib.rcParams.update({
            "pgf.texsystem": "xelatex",
            'text.usetex': True,
            'pgf.rcfonts': False,
            "font.family": "mononoki Nerd Font Mono",
            "font.serif": [],
            #  "font.cursive": ["mononoki Nerd Font", "mononoki Nerd Font Mono"],
        })
        plt.savefig(os.path.join("./output", output, f"{testname}.pgf"))
    plt.show()

