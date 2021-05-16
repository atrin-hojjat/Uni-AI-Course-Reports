import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import math
import os
#  from dotenv import load_dotenv
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import matplotlib
#  matplotlib.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns


#  load_dotenv()

dataset_folder = os.getenv("DATASET_FOLDER", '../Datasets/ml-latest-small/')

training = pd.read_csv(os.path.join(dataset_folder, "ratings.training.csv"))
test = pd.read_csv(os.path.join(dataset_folder, "ratings.test.csv"))

training_matrix = training.pivot(index="movieId", columns="userId",
        values="rating").fillna(0)
test_matrix = test.pivot(index="movieId", columns="userId",
        values="rating").fillna(0)

training_csr = csr_matrix(training_matrix)


user_avg = training.groupby(by="userId").mean()
movie_avg = training.groupby(by="movieId").mean()
global_avg = training.mean()['rating']

training_np = training_matrix.to_numpy()
distances = np.matmul(training_np, training_np.transpose())

distances_diagonal = 1. / np.diagonal(distances).copy()

norm_size_mul = np.sqrt(np.outer(distances_diagonal, distances_diagonal))

cosine_distances = np.multiply(distances, norm_size_mul)

distances_pd = pd.DataFrame(cosine_distances)

bases = (np.ones(training_matrix.values.shape) * -global_avg +
        user_avg.rating.values +
        movie_avg.rating.values.reshape((movie_avg.rating.values.shape[0], 1)))

bases_pd = pd.DataFrame(bases)


dataX, dataErr, dataDErr = [], [], []

for n_neighbors in range(1, 100, 3):
    err, cnt = 0, 0
    derr, dcnt = 0, 0

    NN = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine")

    NN.fit(training_csr)
    for index, row in test.iterrows():
        cnt += 1
        if not (training_matrix.index.values==int(row['movieId'])).any():
            #  print(global_avg, row['rating'])
            err += (global_avg - row['rating']) ** 2
            continue
        if not (training_matrix.index.values==int(row['userId'])).any():
            #  print(global_avg, row['rating'])
            err += (global_avg - row['rating']) ** 2
            continue
        movieInd = np.where(training_matrix.index.values==int(row['movieId']))[0][0]
        userInd = np.where(training_matrix.columns.values==int(row['userId']))[0][0]
        movie = training_matrix.iloc[training_matrix.index==int(row['movieId'])]

        dists, neighbors = NN.kneighbors(movie.values.reshape(1, -1), n_neighbors=n_neighbors)


        #  for neighbor in neighbors[0]:
        #      print(neighbor)

        #      print(userInd)
        #      print(training_matrix.iloc[neighbor, userInd])
        #      print(training_matrix.iloc[neighbor,
        #              training_matrix.columns==int(row['userId'])])

        neighbors = [neighbor for neighbor in neighbors[0] if
                training_matrix.iloc[neighbor, userInd] > 0]

        baseline = (global_avg +
                movie_avg.iloc[movie_avg.index==int(row['movieId'])].values[0] +
                user_avg.iloc[user_avg.index==int(row['userId'])].values[0])


        if len(neighbors) == 0:
            #  print(global_avg, row['rating'])
            err += (global_avg - row['rating']) ** 2
            continue


        neigh_dists_all = distances_pd.iloc[neighbors]
        neigh_dists = neigh_dists_all.iloc[:, movieInd]

        #  print("**********")
        #  print()
        #  print()

        #  print(row)

        #  print(neighbors)
        #  print(neigh_dists)

        bases_nec = bases_pd.iloc[neighbors].loc[:,
                userInd]

        ratings_nec = training_matrix.iloc[neighbors].iloc[:,
                training_matrix.columns==int(row['userId'])]


        ans = bases[movieInd, userInd] + np.inner(ratings_nec.values.reshape(1, -1) -
                bases_nec.values.reshape(1, -1),
                neigh_dists.values.reshape(1, -1)) / np.sum(neigh_dists.values)

        #  print("Base", bases[movieInd, userInd])
        #  print("Rating vec", ratings_nec.values.reshape(1, -1))
        #  print("Base vec",bases_nec.values.reshape(1, -1))
        #  print("Distances", neigh_dists.values.reshape(1, -1))
        #  print("Inner", np.inner(ratings_nec.values.reshape(1, -1) -
        #          bases_nec.values.reshape(1, -1),
        #          neigh_dists.values.reshape(1, -1)))
        #  print("Dividend", np.sum(neigh_dists.values))


        #  print(ans, row['rating'])
        err += (ans - row['rating']) ** 2
        derr += (ans - row['rating']) ** 2
        dcnt += 1
        #  print()
        #  print()

    print("**************")
    print(f"Neighbors: {n_neighbors}")
    print("Error with mean cases: ", math.sqrt(err / cnt))
    print("Error on calculated cases: ", math.sqrt(derr / dcnt) if dcnt > 0 else 0)
    dataX.append(n_neighbors)
    dataErr.append(math.sqrt(err / cnt))
    dataDErr.append(False)
    dataX.append(n_neighbors)
    dataErr.append(math.sqrt(derr / dcnt) if dcnt > 0 else 0)
    dataDErr.append(True)
    print("**************")

testname = "Error by No. neighbors"
y_lab = "Mean squared error"
x_lab = "No. Neighbors"

plt.figure()
sns.relplot(data=pd.DataFrame({"n_n": dataX, "er": dataErr, "From Data": dataDErr}), hue="From Data", x="n_n", y="er", kind="line", )

plt.title(testname)
plt.xlabel(x_lab)
plt.ylabel(y_lab)

if os.getenv("OUTPUT"):
    output = os.getenv("OUTPUT")
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


    

