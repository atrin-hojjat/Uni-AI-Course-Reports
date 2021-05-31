import os
import matplotlib
if os.environ.get('LATEX_OUTPUT', '0') == '1':
    matplotlib.use("pgf")

from Tests import tests

while True:
    for i in range(len(tests)):
        print(f"{i}: {tests[i][0]}")
    answer = int(input("What test do you want to run(-1 to quit)? "))

    if answer < 0: 
        break
    tests[answer][1].run()
