import networkx as nx
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import matplotlib
#  matplotlib.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import os
import numpy as np
import rich
import seaborn as sns

def SetupLibraries():
    matplotlib.rcParams.update({
        "pgf.texsystem": "xelatex",
        'text.usetex': True,
        'pgf.rcfonts': False,
        "font.family": "mononoki Nerd Font Mono",
        "font.serif": [],
        #  "font.cursive": ["mononoki Nerd Font", "mononoki Nerd Font Mono"],
    })

def visualize_line(testname, x_lab, y_lab, ls, output=None, hue="Runner"):
    plt.figure()
    plt.title(testname)

    sns.relplot(data=ls, hue=hue, x=x_lab, y=y_lab, kind="line", style="event")

    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
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

