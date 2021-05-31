import timeit
from sklearn import metrics
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from datasets.mushrooms import LoadMushrooms

from models.Perceptron import Perceptron


def plot(testname):
    if not os.path.exists(os.path.dirname(os.path.join("./output",
        f"{testname}.jpg"))):
        try: os.makedirs(os.path.dirname(os.path.join("./output",
            f"{testname}.jpg")))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    plt.savefig(os.path.join("./output", f"{testname}.jpg"))
    if os.environ.get('LATEX_OUTPUT', '0') == '1':
        matplotlib.rcParams.update({
            "pgf.texsystem": "xelatex",
            'text.usetex': True,
            'pgf.rcfonts': False,
            "font.family": "mononoki Nerd Font Mono",
            "font.serif": [],
            #  "font.cursive": ["mononoki Nerd Font", "mononoki Nerd Font Mono"],
        })
        plt.savefig(os.path.join("./output", f"{testname}.pgf"))
    plt.show()


def max_iters_test():
    X_train, X_test, y_train, y_test, mushrooms, input_data, output_data = LoadMushrooms()

    neighbors, accuracy, precision_0, precision_1, f1_0, f1_1, time = [], [], [], [], [], [], []
    

    for i in range(10, 2000, 20):
        classifier = Perceptron(X_train, y_train, 'perceptron_mushroom',
                input_data.columns, tolerance=1e-8, max_iter=i)
        start = timeit.default_timer()
        classifier.train()
        stop = timeit.default_timer()

        res = metrics.classification_report(y_test, classifier.predict(X_test),
                output_dict=True)

        neighbors.append(i)
        precision_0.append(res['0.0']['precision'])
        precision_1.append(res['1.0']['precision'])
        f1_0.append(res['0.0']['f1-score'])
        f1_1.append(res['1.0']['f1-score'])
        accuracy.append(res['accuracy'])
        time.append(stop - start)

    plt.figure()
    plt.title("Perceptron accuracy measures by increasing maximum number of iterations")
    colors = ["#112233", "#66CC99", "#44BBFF", "#FC575E", "#c955f7"]
    plt.plot(neighbors, precision_0, colors[0], label="Precision for label 0",
            linewidth=1)
    plt.plot(neighbors, precision_1, colors[1], label="Precision for label 1",
            linewidth=1)
    plt.plot(neighbors, f1_0, colors[2], label="F1 score for label 0",
            linewidth=1)
    plt.plot(neighbors, f1_1, colors[3], label="F1 score for label 1",
            linewidth=1)
    plt.plot(neighbors, accuracy, colors[4], label="Accuracy",
            linewidth=1)
    plt.xlabel("Max Iterations")

    plt.legend()
    plot("Perceptron accuracy by increasing maximum number of iterations")

    plt.figure()
    plt.title("Perceptron time by increasing maximum number of iterations")
    colors = ["#112233", "#66CC99", "#44BBFF", "#FC575E", "#c955f7"]
    plt.plot(neighbors, time, colors[0], label="Time",
            linewidth=1)
    plt.xlabel("Max Iterations")
    plt.ylabel("Time")

    plot("Perceptron time by increasing maximum number of iterations")


def tolerance_test():
    X_train, X_test, y_train, y_test, mushrooms, input_data, output_data = LoadMushrooms()

    neighbors, accuracy, precision_0, precision_1, f1_0, f1_1, time = [], [], [], [], [], [], []
    

    tol = 1
    for i in range(10):
        classifier = Perceptron(X_train, y_train, 'perceptron_mushroom',
                input_data.columns, tolerance=tol, max_iter=500)
        start = timeit.default_timer()
        classifier.train()
        stop = timeit.default_timer()

        res = metrics.classification_report(y_test, classifier.predict(X_test),
                output_dict=True)

        neighbors.append(tol)
        precision_0.append(res['0.0']['precision'])
        precision_1.append(res['1.0']['precision'])
        f1_0.append(res['0.0']['f1-score'])
        f1_1.append(res['1.0']['f1-score'])
        accuracy.append(res['accuracy'])
        time.append(stop - start)
        tol = tol / 10


    plt.figure()
    plt.title("Perceptron accuracy measures by tolerance")
    colors = ["#112233", "#66CC99", "#44BBFF", "#FC575E", "#c955f7"]
    plt.plot(neighbors, precision_0, colors[0], label="Precision for label 0",
            linewidth=1)
    plt.plot(neighbors, precision_1, colors[1], label="Precision for label 1",
            linewidth=1)
    plt.plot(neighbors, f1_0, colors[2], label="F1 score for label 0",
            linewidth=1)
    plt.plot(neighbors, f1_1, colors[3], label="F1 score for label 1",
            linewidth=1)
    plt.plot(neighbors, accuracy, colors[4], label="Accuracy",
            linewidth=1)
    plt.xlabel("Tolerance")
    plt.xscale('log')

    plt.legend()
    plot("Perceptron accuracy by tolerance")

    plt.figure()
    plt.title("Perceptron time by tolerance")
    colors = ["#112233", "#66CC99", "#44BBFF", "#FC575E", "#c955f7"]
    plt.plot(neighbors, time, colors[0], label="Time",
            linewidth=1)
    plt.xlabel("Tolerance")
    plt.xscale('log')
    plt.ylabel("Time")

    plot("Perceptron time by tolerance")

def eta0_test():
    X_train, X_test, y_train, y_test, mushrooms, input_data, output_data = LoadMushrooms()

    neighbors, accuracy, precision_0, precision_1, f1_0, f1_1, time = [], [], [], [], [], [], []
    

    for i in np.arange(0.01, 1.1, 0.02):
        classifier = Perceptron(X_train, y_train, 'perceptron_mushroom',
                input_data.columns, eta0=i)
        start = timeit.default_timer()
        classifier.train()
        stop = timeit.default_timer()

        res = metrics.classification_report(y_test, classifier.predict(X_test),
                output_dict=True)

        neighbors.append(i)
        precision_0.append(res['0.0']['precision'])
        precision_1.append(res['1.0']['precision'])
        f1_0.append(res['0.0']['f1-score'])
        f1_1.append(res['1.0']['f1-score'])
        accuracy.append(res['accuracy'])
        time.append(stop - start)

    plt.figure()
    plt.title("Perceptron accuracy measures by learning rate")
    colors = ["#112233", "#66CC99", "#44BBFF", "#FC575E", "#c955f7"]
    plt.plot(neighbors, precision_0, colors[0], label="Precision for label 0",
            linewidth=1)
    plt.plot(neighbors, precision_1, colors[1], label="Precision for label 1",
            linewidth=1)
    plt.plot(neighbors, f1_0, colors[2], label="F1 score for label 0",
            linewidth=1)
    plt.plot(neighbors, f1_1, colors[3], label="F1 score for label 1",
            linewidth=1)
    plt.plot(neighbors, accuracy, colors[4], label="Accuracy",
            linewidth=1)
    plt.xlabel("Learning rate")

    plt.legend()
    plot("Perceptron accuracy by Learning rate")

    plt.figure()
    plt.title("Perceptron time by Learning rate")
    colors = ["#112233", "#66CC99", "#44BBFF", "#FC575E", "#c955f7"]
    plt.plot(neighbors, time, colors[0], label="Time",
            linewidth=1)
    plt.xlabel("Learning rate")
    plt.ylabel("Time")

    plot("Perceptron time by Learning rate")

def run():
    max_iters_test()
    tolerance_test()
    eta0_test()
