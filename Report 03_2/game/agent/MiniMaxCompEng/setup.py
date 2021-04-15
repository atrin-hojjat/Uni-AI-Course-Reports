from distutils.core import setup, Extension
import os
import shutil
import numpy

os.environ["CC"] = "g++"
os.environ["CXX"] = "g++"


module1 = Extension('MiniMax',
                    sources=['calc_minimax_eng.cpp'],
                    language="c++17",
                    include_dirs=[numpy.get_include()],
                    extra_compile_args=["-std=c++17", "-Wall", "-Wextra"],
                    )

setup(name='MiniMaxCppExtension',
       version='0.1',
       description='Calculates Minimax for othello',
       ext_modules=[module1])


#  shutil.copyfile("./build/lib*", "../../../")
