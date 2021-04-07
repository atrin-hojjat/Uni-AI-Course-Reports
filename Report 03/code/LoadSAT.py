from SAT import Genetic, Annealing, HillClimbing, LocalBeamSearch
from visualizers.GraphVisualizers import visualize_tsp
from generators import gen_sat
import rich

def load_samples():
    n = 20

    def check_answer(sat, state):
        cnt = 0
        for i in sat:
            for j in i:
                if state[abs(j) - 1] == (j > 0):
                    cnt += 1
                    break
        return cnt

    sat = gen_sat(variables=n, p=0.2)
    #  rich.print(sat, f"Variables: {n}, Clauses: {len(sat)}")

    for i in range(10):
        rich.print("Annealing")
        path, steps, value = Annealing.annealing_search(n, sat)
        #  rich.print(path, steps, value)
        rich.print("Number of correct clauses: ", check_answer(sat, path))

        rich.print("Hill-climbing")
        path, steps, value = HillClimbing.hill_climbing(n, sat)
        #  rich.print(path, steps, value)
        rich.print("Number of correct clauses: ", check_answer(sat, path))

        rich.print("Local Beam Search")
        path, steps, value = LocalBeamSearch.local_beam_search(n, sat,
                max_iters=1000)
        #  rich.print(path, steps, value)
        rich.print("Number of correct clauses: ", check_answer(sat, path))

        rich.print("Genetic Algorithm")
        path, steps, fitness = Genetic.genetic_algorithm(n, sat, max_iters=1000)
        #  rich.print(path, steps, fitness)
        rich.print("Number of correct clauses: ", check_answer(sat, path))
