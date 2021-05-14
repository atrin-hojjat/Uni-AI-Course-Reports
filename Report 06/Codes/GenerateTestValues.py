import pandas as pd
import numpy as np


def generate_tests_for_movies():
    ratings = pd.read_csv("../Datasets/ml-latest-small/ratings.csv")

    users = ratings.groupby(by="userId").count()
    movies = ratings.groupby(by="movieId").count()

    test_users = users.sample(frac=0.1)
    test_movies = movies.sample(frac=0.1)

    test_ratings = ratings[ratings.userId.isin(test_users.index) &
            ratings.movieId.isin(test_movies.index)]
    training_ratings = ratings[(~ratings.userId.isin(test_users.index)) |
            ~ratings.movieId.isin(test_movies.index)]


    test_ratings.to_csv('../Datasets/ml-latest-small/ratings.test.csv')
    training_ratings.to_csv('../Datasets/ml-latest-small/ratings.training.csv')

if __name__ == '__main__':
    generate_tests_for_movies()
