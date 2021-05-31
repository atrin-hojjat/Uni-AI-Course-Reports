import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
import os
import matplotlib
import matplotlib.pyplot as plt
from models.Model import Model

class DecisionTree(Model):
    def __init__(self, X, y, name, feature_names, criterion="gini", splitter="best",
            max_depth=2, min_samples_leaf=1):
        self.X = X
        self.y = y
        self.model = DecisionTreeClassifier(criterion=criterion, splitter=splitter,
                max_depth=max_depth, min_samples_leaf=min_samples_leaf)
        self.name = name
        self.feature_names = feature_names

    def train(self):
        self.model.fit(self.X, self.y)

    def predict(self, data):
        return self.model.predict(data)

    def save_output(self):
        plt.figure()
        fig, axes = plt.subplots(nrows=1, ncols=1,
                figsize=(5, 5), dpi=900)
        dec_tree = plot_tree(decision_tree=self.model, feature_names=self.feature_names, 
                             filled=True , precision=4, rounded=True, ax=axes)
        if not os.path.exists(os.path.dirname(os.path.join("./output",
            f"{self.name}.jpg"))):
            try: os.makedirs(os.path.dirname(os.path.join("./output",
                f"{self.name}.jpg")))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        plt.savefig(os.path.join("./output", f"{self.name}.jpg"))
        if os.environ.get('LATEX_OUTPUT', '0') == '1':
            matplotlib.rcParams.update({
                "pgf.texsystem": "xelatex",
                'text.usetex': True,
                'pgf.rcfonts': False,
                "font.family": "mononoki Nerd Font Mono",
                "font.serif": [],
                #  "font.cursive": ["mononoki Nerd Font", "mononoki Nerd Font Mono"],
            })
            plt.savefig(os.path.join("./output", f"{self.name}.pgf"))
        plt.show()
