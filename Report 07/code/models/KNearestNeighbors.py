import pandas as pd
from sklearn.neighbors import KNeighbors
import os
import matplotlib.pyplot as plt
from models.Model import Model


class KNearestNeighbors(Model):
    def __init__(self, X, y, name, feature_names, n_neighbors=6):
        self.X = X
        self.y = y
        self.model = KNeighbors(n_neighbors=n_neighbors, n_jobs=4)
        self.name = name
        self.feature_names = feature_names

    def train(self):
        self.model.fit(self.X, self.y)

    def predict(self, data):
        return self.model.predict(data)
