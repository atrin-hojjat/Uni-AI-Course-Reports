import timeit
from sklearn import metrics

from datasets.mushrooms import LoadMushrooms

from models.DecisionTree import DecisionTree
from models.RandomForest import RandomForest


def run():
    X_train, X_test, y_train, y_test, mushrooms, input_data, output_data = LoadMushrooms()

    decision_tree_classifier = DecisionTree(X_train, y_train, 'decision_tree_mushroom',
            input_data.columns)
    random_forest_classifier = RandomForest(X_train, y_train, 'random_forest_mushroom',
            input_data.columns)


    time_data = {}


    def time(f, data, name):
        start = timeit.default_timer()

        f()

        stop = timeit.default_timer()

        data[name] = stop - start

    print("Running Decision Tree")
    time(decision_tree_classifier.train, time_data, 'decision_tree')
    decision_tree_classifier.save_output()

    print("Classification report\n", metrics.classification_report(y_test,
        decision_tree_classifier.predict(X_test)))


    print("Running Random Forest")
    time(random_forest_classifier.train, time_data, 'random_forest')
    random_forest_classifier.save_output()

    print("Classification report\n", metrics.classification_report(y_test,
        random_forest_classifier.predict(X_test)))


    print("Running Single Layered Perceptron")


    print("Time:", time_data)
