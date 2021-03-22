import networkx as nx
import matplotlib.pyplot as plt
import os
def plot_data(testname, x_lab, y_lab, ls, output=None):
    plt.title(testname)
    colors = ["#112233", "#66CC99", "#44BBFF", "#FC575E", "#c955f7"]
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
    plt.show()

