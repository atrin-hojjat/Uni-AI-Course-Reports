# Report 02: Implementing Heuristic algorithms on Vertex cover problem
## Algorithms implemented
- A* search
- Greedy best-first search
- Hill-climbing
- Annealing
Codes for implementation can be found [here](https://github.com/atrin-hojjat/Uni-AI-Course-Reports/blob/master/Problem%2001%20-%20Vertext%20Cover/solutions). 
The input is randomly generated with two different functions([code](https://github.com/atrin-hojjat/Uni-AI-Course-Reports/blob/master/Problem%2001%20-%20Vertext%20Cover/generators)) and the output is generated with matplotlib and networkx libraries([code](https://github.com/atrin-hojjat/Uni-AI-Course-Reports/blob/master/Problem 01%20-%20Vertext%20Cover/visualizers)).
The tests folder is used for generating sample output data. TestIterations runs each algorithm on graphs with different size and compares the results in terms of correctness and time complexity for different generation parameters.
RunSamples generates a few graphs with different size in order to compare the results of each algorithm for a given graph.
