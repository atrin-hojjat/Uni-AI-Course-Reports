from solutions import AStar, GreedyBestFirst, HillClimbing, AnnealingSearch
from generators import *
from visualizers.GraphVisualize import visualize_vertex_cover
import os

def Test(save=False):
    TestGenWithRandomEdges(20, 0.3, save)
    TestGenWithRandomEdges(20, 0.2, save)
    TestGenWithRandomEdges(20, 0.12, save)
    #  TestGenWithRandomEdges(20, 0.1, save)
    TestGenWithRandomEdges(30, 0.2, save)
    TestGenWithRandomEdges(30, 0.12, save)

    #  TestGenWithConstantEdges(20, 10, save)
    #  TestGenWithConstantEdges(20, 50, save)
    TestGenWithConstantEdges(20, 100, save)
    TestGenWithConstantEdges(30, 40, save)
    TestGenWithConstantEdges(20, 140, save)
    #  thread.start_new_thread(TestGenWithRandomEdges, (20, 0.3,
    #      save))
    #  thread.start_new_thread(TestGenWithRandomEdges, (20, 0.2,
    #      save))
    #  thread.start_new_thread(TestGenWithRandomEdges, (20, 0.12,
    #      save))
    #  thread.start_new_thread(TestGenWithRandomEdges, (20, 0.1,
    #      save))
    #  thread.start_new_thread(TestGenWithRandomEdges, (30, 0.2,
    #      save))
    #  thread.start_new_thread(TestGenWithRandomEdges, (30, 0.12,
    #      save))

    #  thread.start_new_thread(TestGenWithConstantEdges, (20, 10,
    #      save))
    #  thread.start_new_thread(TestGenWithConstantEdges, (20, 50,
    #      save))
    #  thread.start_new_thread(TestGenWithConstantEdges, (20, 100,
    #      save))
    #  thread.start_new_thread(TestGenWithConstantEdges, (30, 40,
    #      save))
    #  thread.start_new_thread(TestGenWithConstantEdges, (20, 140,
    #      save))

def TestGenWithRandomEdges(N=20, P=0.12, save=False):
    output = None
    if save:
        output = f"{N}-{P}"
    graph = gen_graph_eq_prob_edges(nodes=N, p=P)

    TestGraph(graph, output=output)

def TestGenWithConstantEdges(N=20, E=80, save=False):
    output = None
    if save:
        output = f"{N}-{E}"
    graph = gen_graph_fix_set_edges(nodes=N, edges=E)

    TestGraph(graph, output=output)

def TestGraph(g, output=None):
    astar_ans, astar_steps = AStar.Astar(g)
    gbfs_ans, gbfs_steps = GreedyBestFirst.greedy_bestfirst_search(g)
    hc_ans, hc_steps = HillClimbing.hill_climbing(g)
    hc_rnd_08_ans, hc_rnd_08_steps = HillClimbing.hill_climbing(g, 0.08)
    annealing_ans, annealing_steps = AnnealingSearch.annealing_search(g)
    annealing_rnd_08_ans, annealing_rnd_08_steps = AnnealingSearch.annealing_search(g, rand_start=0.08)


    print("------Answers------")
    print("A*: ", astar_ans, len(astar_ans), f"In {astar_steps} itarations")
    print("Greedy Best-first search: ", gbfs_ans, len(gbfs_ans), 
            f"In {gbfs_steps} itarations")
    print("Hill-Climbing: ", hc_ans, len(hc_ans), f"In {hc_steps} itarations")
    print("Hill-Climbing with random start: ", hc_rnd_08_ans,
            len(hc_rnd_08_ans), f"In {hc_rnd_08_steps} itarations")
    print("Simulated Annealing search: ", annealing_ans,
            len(annealing_ans), f"In {annealing_steps} itarations")
    print("Simulated Annealing searchwith random start: ",
            annealing_rnd_08_ans, len(annealing_rnd_08_ans), 
            f"In {annealing_rnd_08_steps} itarations")
    if output:
        if not os.path.exists(os.path.dirname(os.path.join("./output", output, "stats"))):
            try: os.makedirs(os.path.dirname(os.path.join("./output", output, "stats")))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        f = open(os.path.join("./output", output, "stats"), 'w')

        f.write(" ".join(["------Answers------"]))
        f.write("\n")
        f.write(" ".join(["A*: ", str(astar_ans), str(len(astar_ans)), 
            f"In {astar_steps} itarations"]))
        f.write("\n")
        f.write(" ".join(["Greedy Best-first search: ", str(gbfs_ans),
            str(len(gbfs_ans)), 
                f"In {gbfs_steps} itarations"]))
        f.write("\n")
        f.write(" ".join(["Hill-Climbing: ", str(hc_ans),
            str(len(hc_ans)), 
            f"In {hc_steps} itarations"]))
        f.write("\n")
        f.write(" ".join(["Hill-Climbing with random start: ",
            str(hc_rnd_08_ans), 
                str(len(hc_rnd_08_ans)), 
                f"In {hc_rnd_08_steps} itarations"]))
        f.write("\n")
        f.write(" ".join(["Simulated Annealing search: ",
            str(annealing_ans), 
                str(len(annealing_ans)), 
                f"In {annealing_steps} itarations"]))
        f.write("\n")
        f.write(" ".join(["Simulated Annealing searchwith random start: ",
                str(annealing_rnd_08_ans),
                str(len(annealing_rnd_08_ans)), 
                f"In {annealing_rnd_08_steps} itarations"]))
        f.write("\n")
        f.close()

    visualize_vertex_cover(g, astar_ans, name=f"A* Results graph {output}", output=output)
    visualize_vertex_cover(g, gbfs_ans, name=f"Greedy best-first search Results graph {output}", output=output)
    visualize_vertex_cover(g, hc_ans, name=f"Hill-Climbing Results graph {output}", output=output)
    visualize_vertex_cover(g, hc_rnd_08_ans, name=f"Hill-Climbing with random start(0.08) Results graph {output}", output=output)
    visualize_vertex_cover(g, annealing_ans, name=f"Annealing Search Results graph {output}", output=output)
    visualize_vertex_cover(g, annealing_rnd_08_ans, name=f"Annealing Search with randmo start(0.08) Resultsngraph {output}", output=output)
