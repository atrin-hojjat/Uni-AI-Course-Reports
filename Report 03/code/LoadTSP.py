from TSP import Genetic, Annealing, HillClimbing, LocalBeamSearch
from generators import gen_weighted_graph, gen_sat
import rich
from tests import TestTSPByNodes

def load_samples():
    from visualizers.GraphVisualizers import visualize_tsp
    graph = gen_weighted_graph(nodes=10)
    rich.print(graph)

    rich.print("Annealing")
    path, steps, value = Annealing.annealing_search(graph)
    rich.print(path, steps, value)
    visualize_tsp(graph, path=path, name="Simulated Annealing Search", output="Sample 20 nodes")

    rich.print("Hill-climbing")
    path, steps, value = HillClimbing.hill_climbing(graph)
    rich.print(path, steps, value)
    visualize_tsp(graph, path=path, name="Hill-Climbing", output="Sample 20 nodes")

    rich.print("Local Beam Search")
    path, steps, value = LocalBeamSearch.local_beam_search(graph)
    rich.print(path, steps, value)
    visualize_tsp(graph, path=path, name="Local Beam Search", output="Sample 20 nodes")

    rich.print("Genetic Algorithm")
    path, steps, fitness = Genetic.genetic_algorithm(graph, max_iters=1000)
    rich.print(path, steps, fitness)
    visualize_tsp(graph, path=path, name="Genetic Algorithm", output="Sample 20 nodes")

def run_tests():
    TestTSPByNodes.test_tsp_by_nodes(start=15, end=20, diff=2, output="Test TSP by N")

