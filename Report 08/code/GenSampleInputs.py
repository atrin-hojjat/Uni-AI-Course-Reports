import tensorflow as tf
import numpy as np
import os

import matplotlib
if os.environ.get('LATEX_OUTPUT', '0') == '1':
    matplotlib.use("pgf")

import matplotlib.pyplot as plt

(X, y), (X_test, y_test) = tf.keras.datasets.mnist.load_data()

print(X)
print(X.shape)

for i in range(10):
    plt.figure()
    pixels = np.array(X[i], dtype='uint8')
    pixels = pixels.reshape((28, 28))

    testname = f"input{i}_label{y[i]}"
    plt.imshow(pixels, cmap='gray')

    if not os.path.exists(os.path.dirname(os.path.join("./output", 'samples',
        f"{testname}.jpg"))):
        try: os.makedirs(os.path.dirname(os.path.join("./output", 'samples',
            f"{testname}.jpg")))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    plt.savefig(os.path.join("./output", 'samples', f"{testname}.jpg"))
    if os.environ.get('LATEX_OUTPUT', '0') == '1':
        matplotlib.rcParams.update({
            "pgf.texsystem": "xelatex",
            'text.usetex': True,
            'pgf.rcfonts': False,
            "font.family": "mononoki Nerd Font Mono",
            "font.serif": [],
            #  "font.cursive": ["mononoki Nerd Font", "mononoki Nerd Font Mono"],
        })
        plt.savefig(os.path.join("./output", 'samples', f"{testname}.pgf"))



    plt.show()

