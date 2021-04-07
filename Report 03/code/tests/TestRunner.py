import os
import numpy as np
from rich.progress import track
import pandas as pd
from visualizers.DataVisualizers import visualize_line

def run(name, points, runners, generator, tests_per_point=10, ret_data=lambda x, y, z: x,
        data_names=[], x_name="X", output=None, **kwargs):
    res = []

    for point in track(np.arange(*points)):
        for i in range(tests_per_point):
            test = generator(point)
            for name, runner in runners.items():
                result = runner(test, **kwargs)
                fix_res = point, *ret_data(result, test, name), name

                res.append(fix_res)



    np_arr = np.array(res)
    dataset = pd.DataFrame(np_arr, columns=[x_name, *data_names, "Runner"])

    for i in data_names: 
        visualize_line(f"{name}: {i}", x_name, i, dataset, output=output, hue="Runner")

