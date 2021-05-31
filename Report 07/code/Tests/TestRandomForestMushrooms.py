import timeit
from sklearn import metrics
import os
import matplotlib
import matplotlib.pyplot as plt

from datasets.mushrooms import LoadMushrooms

from models.RandomForest import RandomForest


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


def max_depth_test():
    X_train, X_test, y_train, y_test, mushrooms, input_data, output_data = LoadMushrooms()

    neighbors, accuracy, precision_0, precision_1, f1_0, f1_1, time = [], [], [], [], [], [], []
    

    for i in range(1, 8):
        classifier = RandomForest(X_train, y_train, 'random_forest_mushroom',
                input_data.columns, max_depth=i)
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
    plt.title("Random Forest measures by tree depth")
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
    plt.xlabel("Max Depth")

    plt.legend()
    plot("Random Forest measures by Max Depth")

    plt.figure()
    plt.title("Random Forest running time by tree depth")
    colors = ["#112233", "#66CC99", "#44BBFF", "#FC575E", "#c955f7"]
    plt.plot(neighbors, time, colors[0], label="Time",
            linewidth=1)
    plt.xlabel("Max Depth")
    plt.ylabel("Time")

    plot("Random Forest running time by Max Depth")

def n_estimators_test():
    X_train, X_test, y_train, y_test, mushrooms, input_data, output_data = LoadMushrooms()

    neighbors, accuracy, precision_0, precision_1, f1_0, f1_1, time = [], [], [], [], [], [], []
    

    for i in range(10, 110, 10):
        classifier = RandomForest(X_train, y_train, 'random_forest_mushroom',
                input_data.columns, n_estimators=i)
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
    plt.title("Random Forest measures by No. Estimators")
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
    plt.xlabel("No. Estimators")

    plt.legend()
    plot("Random Forest measures by No. Estimators")

    plt.figure()
    plt.title("Random Forest running time by No. Estimators")
    colors = ["#112233", "#66CC99", "#44BBFF", "#FC575E", "#c955f7"]
    plt.plot(neighbors, time, colors[0], label="Time",
            linewidth=1)
    plt.xlabel("No. Estimators")
    plt.ylabel("Time")

    plot("Random Forest running time by No. Estimators")


def run():
    max_depth_test()
    n_estimators_test()
