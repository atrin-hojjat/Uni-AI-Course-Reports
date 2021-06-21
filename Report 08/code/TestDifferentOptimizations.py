import tensorflow as tf
import numpy as np
import os
import rich

import matplotlib
if os.environ.get('LATEX_OUTPUT', '0') == '1':
    matplotlib.use("pgf")

import matplotlib.pyplot as plt


batch_size, epochs = 100, 10

def load_data():
    (X, y), (X_test, y_test) = tf.keras.datasets.mnist.load_data()

    return (X, y), (X_test, y_test)

def load_data_with_expandedd_labels():
    (X, y), (X_test, y_test) = load_data()

    ny = np.array([[j == i for j in range(10)] for i in y])
    ny_test = np.array([[j == i for j in range(10)] for i in y_test])
    print(y[0])
    print(ny[0])

    return (X, ny), (X_test, ny_test)



def create_simple_model(name=None):
    model = tf.keras.Sequential(
            [
                tf.keras.layers.Flatten(input_shape=(28, 28)),
                tf.keras.layers.Dense(1000, activation='sigmoid'),
                tf.keras.layers.Dense(500, activation='sigmoid'),
                tf.keras.layers.Dense(100, activation='sigmoid'),
                tf.keras.layers.Dense(50, activation='sigmoid'),
                tf.keras.layers.Dense(10, activation='softmax'),
            ],
            name=name,
        )

    return model

def compile_simple_model(name, optimizer, loss='categorical_crossentropy',
        metrics=[
            'mean_squared_error',
            'accuracy', 
            tf.keras.metrics.Precision(),
            tf.keras.metrics.Recall(),
            ]):
    model = create_simple_model(name)
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    return model

def create_large_model(name=None):
    model = tf.keras.Sequential(
            [
                tf.keras.layers.Flatten(input_shape=(28, 28)),
                tf.keras.layers.Dense(2000, activation='sigmoid'),
                tf.keras.layers.Dense(1300, activation='sigmoid'),
                tf.keras.layers.Dense(800, activation='sigmoid'),
                tf.keras.layers.Dense(100, activation='sigmoid'),
                tf.keras.layers.Dense(10, activation='softmax'),
            ],
            name=name,
        )

    return model

def compile_large_model(name, optimizer, loss='categorical_crossentropy',
        metrics=[
            'mean_squared_error',
            'accuracy', 
            tf.keras.metrics.Precision(),
            tf.keras.metrics.Recall(),
            ]):
    model = create_large_model(name)
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    return model


def create_cnn_model(name=None):
    model = tf.keras.Sequential(
            [
                tf.keras.Input(shape=(28 * 28, )),
                tf.keras.layers.Dense(570, activation='sigmoid'),
                tf.keras.layers.Dense(200, activation='sigmoid'),
                tf.keras.layers.Dense(80, activation='sigmoid'),
                tf.keras.layers.Dense(10, activation='softmax'),
            ],
            name=name,
        )

    return model

def compile_cnn_model(name, optimizer, loss='categorical_crossentropy',
        metrics=[
            'mean_squared_error',
            'accuracy', 
            tf.keras.metrics.Precision(),
            tf.keras.metrics.Recall(),
            ]):
    model = create_simple_model(name)
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    return model

def train_model():
    pass

def plot_data(testname, x_lab, y_lab, ls):
    plt.figure()
    plt.title(testname)
    colors = ["#112233", "#66CC99", "#44BBFF", "#FC575E", "#c955f7", "#6C8784",
            "#D98B3A", "#FEC606", "#BADA55", "#C82647", "#83D6DE", "#9684A3"]
    rich.print(ls)
    for x in range(len(ls)):
        val = ls[x]
        plt.plot(val['X'], val['Y'], colors[x], label=val['name'],
                linewidth=1)
        print(x, val)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.legend()
    if not os.path.exists(os.path.dirname(os.path.join("./output",
        f"{testname}.jpg"))):
        try: os.makedirs(os.path.dirname(os.path.join("./output",
            f"{testname}.jpg")))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    plt.savefig(os.path.join("./output", f"{testname}.jpg"))
    if os.environ.get('LATEX_OUTPUT', '0') == '1':
        matplotlib.rcParams.update({
            "pgf.texsystem": "xelatex",
            'text.usetex': True,
            'pgf.rcfonts': False,
            "font.family": "mononoki Nerd Font Mono",
            "font.serif": [],
            #  "font.cursive": ["mononoki Nerd Font", "mononoki Nerd Font Mono"],
        })
        plt.savefig(os.path.join("./output", f"{testname}.pgf"))
    plt.show()

if __name__ == '__main__':
    (X_train, y_train), (X_val, y_val) = load_data_with_expandedd_labels()


    res_acc, res_pre, res_rec, res_loss, res_mse = [], [], [], [], []

    model = compile_simple_model('adam',
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9,
                beta_2=0.999, epsilon=1e-7))
    model.summary()
    hist = model.fit(X_train, y_train, batch_size=batch_size,
            epochs=epochs, validation_data=(X_val, y_val))
    res_acc.append({'X': range(epochs), 'Y': hist.history['accuracy'], 'name':
    'Adam Accuracy'})
    res_acc.append({'X': range(epochs), 'Y': hist.history['val_accuracy'], 'name':
    'Adam Validation Accuracy'})

    res_pre.append({'X': range(epochs), 'Y': hist.history['precision'], 'name':
    'Adam Precision'})
    res_pre.append({'X': range(epochs), 'Y': hist.history['val_precision'], 'name':
    'Adam Validation Precision'})
    
    res_rec.append({'X': range(epochs), 'Y': hist.history['recall'], 'name':
    'Adam Recall'})
    res_rec.append({'X': range(epochs), 'Y': hist.history['val_recall'], 'name':
    'Adam Validation Recall'})

    res_loss.append({'X': range(epochs), 'Y': hist.history['loss'], 'name':
    'Adam Loss'})
    res_loss.append({'X': range(epochs), 'Y': hist.history['val_loss'], 'name':
    'Adam Validation Loss'})

    res_mse.append({'X': range(epochs), 'Y': hist.history['mean_squared_error'], 'name':
    'Adam MSE'})
    res_mse.append({'X': range(epochs), 'Y': hist.history['val_mean_squared_error'], 'name':
    'Adam Validation MSE'})


    rich.print(hist.history)
    

    model = compile_simple_model('sgdmomentum',
            optimizer=tf.keras.optimizers.SGD(learning_rate=0.05, momentum=0.07))
    model.summary()
    hist = model.fit(X_train, y_train, batch_size=batch_size,
            epochs=epochs, validation_data=(X_val, y_val))
    res_acc.append({'X': range(epochs), 'Y': hist.history['accuracy'], 'name':
    'SGD Momentom Accuracy'})
    res_acc.append({'X': range(epochs), 'Y': hist.history['val_accuracy'], 'name':
    'SGD Momentom Validation Accuracy'})

    res_pre.append({'X': range(epochs), 'Y': hist.history['precision'], 'name':
    'SGD Momentom Precision'})
    res_pre.append({'X': range(epochs), 'Y': hist.history['val_precision'], 'name':
    'SGD Momentom Validation Precision'})
    
    res_rec.append({'X': range(epochs), 'Y': hist.history['recall'], 'name':
    'SGD Momentom Recall'})
    res_rec.append({'X': range(epochs), 'Y': hist.history['val_recall'], 'name':
    'SGD Momentom Validation Recall'})

    res_loss.append({'X': range(epochs), 'Y': hist.history['loss'], 'name':
    'SGD Momentom Loss'})
    res_loss.append({'X': range(epochs), 'Y': hist.history['val_loss'], 'name':
    'SGD Momentom Validation Loss'})

    res_mse.append({'X': range(epochs), 'Y': hist.history['mean_squared_error'], 'name':
    'SGD Momentom MSE'})
    res_mse.append({'X': range(epochs), 'Y': hist.history['val_mean_squared_error'], 'name':
    'SGD Momentom Validation MSE'})


    rich.print(hist.history)



    model = compile_simple_model('sgd',
            optimizer=tf.keras.optimizers.SGD(learning_rate=0.05))
    model.summary()
    hist = model.fit(X_train, y_train, batch_size=batch_size,
            epochs=epochs, validation_data=(X_val, y_val))
    res_acc.append({'X': range(epochs), 'Y': hist.history['accuracy'], 'name':
    'SGD Accuracy'})
    res_acc.append({'X': range(epochs), 'Y': hist.history['val_accuracy'], 'name':
    'SGD Validation Accuracy'})

    res_pre.append({'X': range(epochs), 'Y': hist.history['precision'], 'name':
    'SGD Precision'})
    res_pre.append({'X': range(epochs), 'Y': hist.history['val_precision'], 'name':
    'SGD Validation Precision'})
    
    res_rec.append({'X': range(epochs), 'Y': hist.history['recall'], 'name':
    'SGD Recall'})
    res_rec.append({'X': range(epochs), 'Y': hist.history['val_recall'], 'name':
    'SGD Validation Recall'})

    res_loss.append({'X': range(epochs), 'Y': hist.history['loss'], 'name':
    'SGD Loss'})
    res_loss.append({'X': range(epochs), 'Y': hist.history['val_loss'], 'name':
    'SGD Validation Loss'})

    res_mse.append({'X': range(epochs), 'Y': hist.history['mean_squared_error'], 'name':
    'SGD MSE'})
    res_mse.append({'X': range(epochs), 'Y': hist.history['val_mean_squared_error'], 'name':
    'SGD Validation MSE'})

    rich.print(hist.history)


    plot_data("Accuracy", "Epoch", "Value", res_acc)
    plot_data("Recall", "Epoch", "Value", res_rec)
    plot_data("Precision", "Epoch", "Value", res_pre)
    plot_data("Loss", "Epoch", "Value", res_loss)
    plot_data("Mean Squared Error", "Epoch", "Value", res_mse)


