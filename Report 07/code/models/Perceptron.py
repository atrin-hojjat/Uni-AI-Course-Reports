import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.linear_model import Perceptron as PerceptronClassifier
import os
import matplotlib.pyplot as plt
from models.Model import Model


class Perceptron(Model):
    def __init__(self, X, y, name, feature_names, max_iter=1000, tolerance=1e-3,
            eta0=1):
        self.X = X
        self.y = y
        self.model = PerceptronClassifier(max_iter=max_iter, tol=tolerance,
                eta0=eta0, n_jobs=4)
        self.name = name
        self.feature_names = feature_names

    def train(self):
        self.model.fit(self.X, self.y)

    def predict(self, data):
        return self.model.predict(data)
