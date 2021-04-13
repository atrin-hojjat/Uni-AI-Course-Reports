from tests.TestRunner import run
from TSP import Genetic, Annealing, HillClimbing, LocalBeamSearch
from generators import gen_weighted_graph, gen_sat
import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np

tspDll = ctypes.CDLL("./tests/efficient_solvers/tsp")

tspDll.solve.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_int))]
tspDll.solve.restype = ctypes.c_int

graph_prv = None
answer_prv = -1


def best_answer(graph):
    global graph_prv, answer_prv
    if graph == graph_prv:
        return answer_prv
    graph_prv = graph
    _p = ndpointer(dtype=np.int32, ndim=2, shape=(len(graph), len(graph)), flags='C')

    tspDll.solve.argtypes = [ctypes.c_int, _p]
    answer_prv = tspDll.solve(len(graph), np.array(graph, dtype=np.int32,))
    return answer_prv

tot_edges_prv = None
tot_edges_ans = None
def get_tot_edges(graph):
    global tot_edges_prv, tot_edges_ans
    if graph == tot_edges_prv:
        return tot_edges_ans
    tot_edges_ans = 0
    tot_edges_prv = graph
    for i in graph:
        for j in i:
            tot_edges_ans += j
    return tot_edges_ans



def test_tsp_by_nodes(start=3, end=21, diff=1, **kwargs):
    runners = {
            "Annealing": lambda x, **t: Annealing.annealing_search(x,
                min_temprature=0.0001),
            "Hill-Climbing": lambda x, **t: HillClimbing.hill_climbing(x),
            "Local Beam Search": lambda x, **t: LocalBeamSearch.local_beam_search(x, 
                max_iters=1000),
            "Genetic Algorithm": lambda x, **t: Genetic.genetic_algorithm(x,
                max_iters=1000),
            }
    def ret_data_sorter(data, test, runner):
        return data[1], (get_tot_edges(test) - data[2]) / best_answer(test) * 100

    run("Test TSP by No. of vertices", (start, end, diff), 
            runners=runners, generator=gen_weighted_graph, data_names=["No.  Iterations", 
                "% worse than best answer"], ret_data=ret_data_sorter,
            x_name="N", output="TSPN")
    

