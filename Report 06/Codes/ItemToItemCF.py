import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import math


training = pd.read_csv("../Datasets/ml-latest-small/ratings.training.csv")
test = pd.read_csv("../Datasets/ml-latest-small/ratings.test.csv")

training_matrix = training.pivot(index="movieId", columns="userId",
        values="rating").fillna(0)
test_matrix = test.pivot(index="movieId", columns="userId",
        values="rating").fillna(0)

training_csr = csr_matrix(training_matrix)

n_neighbors = 10
NN = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine")

NN.fit(training_csr)

user_avg = training.groupby(by="userId").mean()
movie_avg = training.groupby(by="movieId").mean()
global_avg = training.mean()['rating']

training_np = training_matrix.to_numpy()
distances = np.matmul(training_np, training_np.transpose())

distances_diagonal = 1. / np.diagonal(distances).copy()

norm_size_mul = np.sqrt(np.outer(distances_diagonal, distances_diagonal))

cosine_distances = np.multiply(distances, norm_size_mul)

distances_pd = pd.DataFrame(cosine_distances)

bases = (np.ones(training_matrix.values.shape) * global_avg +
        user_avg.rating.values +
        movie_avg.rating.values.reshape((movie_avg.rating.values.shape[0], 1)))


for index, row in test.iterrows():
    movie = training_matrix.iloc[training_matrix.index==int(row['movieId'])]

    dists, neighbors = NN.kneighbors(movie.values.reshape(1, -1), n_neighbors=n_neighbors)

    baseline = (global_avg +
            movie_avg.iloc[movie_avg.index==int(row['movieId'])].values[0] +
            user_avg.iloc[user_avg.index==int(row['userId'])].values[0])


    neigh_dists_all = distances_pd.iloc[distances_pd.index.isin(neighbors[0])]
    neigh_dists = neigh_dists_all.loc[:, row['movieId']]

    

    break
