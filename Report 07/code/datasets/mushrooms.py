import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import os


def LoadMushrooms(filename=None):
    if filename is None:
        filename = os.environ.get('DATASET_FILE', None)

    if filename is None:
        filename = input("Enter dataset file location: ")

    mushrooms_raw = pd.read_csv(filename)

    encoder = OneHotEncoder(drop="if_binary")
    mushrooms = encoder.fit_transform(mushrooms_raw).toarray()

    categorized_columns = []

    for i in range(len(mushrooms_raw.columns)):
        column_name = mushrooms_raw.columns[i]
        if len(encoder.categories_[i]) > 2:
            for val in encoder.categories_[i]:
                categorized_columns.append(f"{column_name}_{val}")
        else:
            categorized_columns.append(f"{column_name}")
    print(encoder.categories_)

    mushrooms = pd.DataFrame(data=mushrooms, columns=categorized_columns)

    input_data = mushrooms.drop(['class'], axis=1)
    output_data = mushrooms['class']


    X_train, X_test, y_train, y_test = train_test_split(input_data, output_data,
            test_size=0.2, random_state=1)

    return X_train, X_test, y_train, y_test, mushrooms, input_data, output_data

