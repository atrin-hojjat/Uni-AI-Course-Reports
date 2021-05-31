import timeit
from sklearn import metrics

from datasets.mushrooms import LoadMushrooms

from models.DecisionTree import DecisionTree
from models.RandomForest import RandomForest
from models.Perceptron import Perceptron


def run():
    X_train, X_test, y_train, y_test, mushrooms, input_data, output_data = LoadMushrooms()

    decision_tree_classifier = DecisionTree(X_train, y_train, 'decision_tree_mushroom',
            input_data.columns, max_depth=6)
    random_forest_classifier = RandomForest(X_train, y_train, 'random_forest_mushroom',
            input_data.columns, max_depth=6)
    perceptron_classifier = Perceptron(X_train, y_train, 'perceptron_mushroom',
            input_data.columns)
    k_nearest_neighbors_classifier = Perceptron(X_train, y_train, 'knn_mushroom',
            input_data.columns)


    time_data = {}


    def time(f, data, name):
        start = timeit.default_timer()

        f()

        stop = timeit.default_timer()

        data[name] = stop - start

    print("Running Decision Tree")
    time(decision_tree_classifier.train, time_data, 'decision_tree')
    #  decision_tree_classifier.save_output()

    print("Classification report\n", metrics.classification_report(y_test,
        decision_tree_classifier.predict(X_test)))


    print("Running Random Forest")
    time(random_forest_classifier.train, time_data, 'random_forest')
    #  random_forest_classifier.save_output()

    print("Classification report\n", metrics.classification_report(y_test,
        random_forest_classifier.predict(X_test)))


    print("Running Single Layered Perceptron")
    time(perceptron_classifier.train, time_data, 'perceptron')

    print("Classification report\n", metrics.classification_report(y_test,
        perceptron_classifier.predict(X_test)))


    print("Running K-Nearest Neighbors")
    time(k_nearest_neighbors_classifier.train, time_data, 'knn')

    print("Classification report\n", metrics.classification_report(y_test,
        k_nearest_neighbors_classifier.predict(X_test)))


    print("Time:", time_data)
