import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree
import os
import matplotlib
import matplotlib.pyplot as plt
from models.Model import Model

class RandomForest(Model):
    def __init__(self, X, y, name, feature_names, n_estimators=100,
            criterion="gini", min_samples_split=2,
            max_depth=2, min_samples_leaf=1, PLOT_nrows=3, PLOT_ncols=5):
        self.X = X
        self.y = y
        self.model = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, 
                min_samples_split=min_samples_split,
                max_depth=max_depth, min_samples_leaf=min_samples_leaf, n_jobs=4)
        self.name = name
        self.feature_names = feature_names
        self.PLOT_ncols = PLOT_ncols
        self.PLOT_nrows = PLOT_nrows

    def train(self):
        self.model.fit(self.X, self.y)

    def predict(self, data):
        return self.model.predict(data)

    def save_output(self):
        plt.figure()
        fig, axes = plt.subplots(nrows=self.PLOT_nrows, ncols=self.PLOT_ncols,
                figsize=(7, 6), dpi=900)

        for i in range(15):
            dec_tree = plot_tree(decision_tree=self.model.estimators_[i], 
                    feature_names=self.feature_names, 
                     filled=True , precision=4, rounded=True, 
                     ax=axes[int(i / self.PLOT_ncols), i % self.PLOT_ncols])
            axes[int(i / self.PLOT_ncols), i % self.PLOT_ncols].set_title('Estimator: ' + str(i), fontsize = 11)
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
