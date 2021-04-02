from solutions import AStar, GreedyBestFirst, HillClimbing, AnnealingSearch
from generators import *
from visualizers.DataPlot import plot_data, plot_stacked_bar
import os
from rich.progress import track
import numpy
import rich

SMP_DATA = {"X": [], "Y": [], "name": ""}

def GEN_SMP_DATA():
    return {"X": [], "Y": [], "name": ""}

def GEN_SMP_DATA_STACKED(n=4):
    return {"X": [], "Y": [[], [], [], []], "name": ""}

def TestByN(start=5, end=25, diff=2, tries=10, p=.2):
    success_rate = [] 
    iterations = []
    res = [GEN_SMP_DATA(), GEN_SMP_DATA(), GEN_SMP_DATA(),
            GEN_SMP_DATA()]
    res1 = [GEN_SMP_DATA(), GEN_SMP_DATA(), GEN_SMP_DATA(),
            GEN_SMP_DATA()]
    res2 = [GEN_SMP_DATA_STACKED(), GEN_SMP_DATA_STACKED(), GEN_SMP_DATA_STACKED(),
            GEN_SMP_DATA_STACKED()]
    names = ['A*', 'Greedy best-first search',
            'Hill-climbing', 'Annealing']

    for i in range(len(res)):
        res[i]['name'] = names[i]
        res1[i]['name'] = names[i]
        res2[i]['name'] = names[i]
    for n in track(numpy.arange(start, end, diff)):
        avg = [0, 0, 0, 0]
        success = [0, 0, 0, 0]

        for i in range(len(res2)):
            for t in res2[i]['Y']:
                t.append(0)

        for x in range(tries):
            g = gen_graph_eq_prob_edges(nodes=n, p=p)

            astar_ans, astar_steps = AStar.Astar(g)
            gbfs_ans, gbfs_steps = GreedyBestFirst.greedy_bestfirst_search(g)
            hc_ans, hc_steps = HillClimbing.hill_climbing(g)
            annealing_ans, annealing_steps = AnnealingSearch.annealing_search(g)

            avg[0] = avg[0] + astar_steps
            avg[1] = avg[1] + gbfs_steps
            avg[2] = avg[2] + hc_steps
            avg[3] = avg[3] + annealing_steps

            success[0] = success[0] + (1 if len(astar_ans) ==
                    len(astar_ans)
                    else 0)
            success[1] = success[1] + (1 if len(gbfs_ans) ==
                    len(astar_ans) else 0)
            success[2] = success[2] + (1 if len(hc_ans) == len(astar_ans)
                    else 0)
            success[3] = success[3] + (1 if len(annealing_ans) ==
                    len(astar_ans) else 0)

            res2[0]['Y'][max(0, min(3, len(astar_ans) - len(astar_ans)))][-1] += 1
            res2[1]['Y'][max(0, min(3, len(gbfs_ans) - len(astar_ans)))][-1] += 1
            res2[2]['Y'][max(0, min(3, len(hc_ans) - len(astar_ans)))][-1] += 1
            res2[3]['Y'][max(0, min(3, len(annealing_ans) - len(astar_ans)))][-1] += 1

        avg = [x / tries for x in avg]
        success = [x / tries * 100 for x in success]
        for i in range(len(avg)):
            res[i]['X'].append(n)
            res[i]['Y'].append(avg[i])
            res1[i]['X'].append(n)
            res1[i]['Y'].append(success[i])
            res2[i]['X'].append(n)
        success_rate.append(success)
        iterations.append(avg)
    plot_stacked_bar('Distance from best answer', 'N', '\\#',
            res2, 'TestByN')
    plot_data('Test number of iterations by N', 'N', 'Iterations',
            res, 'TestByN')
    plot_data('Test success rate by N', 'N', 'Success rate %',
            res1, 'TestByN')

def TestByP(start=0.1, end=0.5, diff=0.02, tries=10, nodes=20):
    success_rate = [] 
    iterations = []
    res = [GEN_SMP_DATA(), GEN_SMP_DATA(), GEN_SMP_DATA(),
            GEN_SMP_DATA()]
    res1 = [GEN_SMP_DATA(), GEN_SMP_DATA(), GEN_SMP_DATA(),
            GEN_SMP_DATA()]
    names = ['A*', 'Greedy best-first search',
            'Hill-climbing', 'Annealing']
    res2 = [GEN_SMP_DATA_STACKED(), GEN_SMP_DATA_STACKED(), GEN_SMP_DATA_STACKED(),
            GEN_SMP_DATA_STACKED()]

    for i in range(len(res)):
        res[i]['name'] = names[i]
        res1[i]['name'] = names[i]
        res2[i]['name'] = names[i]
    for p in track(numpy.arange(start, end, diff)):
        avg = [0, 0, 0, 0]
        success = [0, 0, 0, 0]

        for i in range(len(res2)):
            for t in res2[i]['Y']:
                t.append(0)

        for n in range(tries):
            g = gen_graph_eq_prob_edges(nodes=nodes, p=p)

            astar_ans, astar_steps = AStar.Astar(g)
            gbfs_ans, gbfs_steps = GreedyBestFirst.greedy_bestfirst_search(g)
            hc_ans, hc_steps = HillClimbing.hill_climbing(g)
            annealing_ans, annealing_steps = AnnealingSearch.annealing_search(g)

            avg[0] = avg[0] + astar_steps
            avg[1] = avg[1] + gbfs_steps
            avg[2] = avg[2] + hc_steps
            avg[3] = avg[3] + annealing_steps

            success[0] = success[0] + (1 if len(astar_ans) ==
                    len(astar_ans)
                    else 0)
            success[1] = success[1] + (1 if len(gbfs_ans) ==
                    len(astar_ans) else 0)
            success[2] = success[2] + (1 if len(hc_ans) == len(astar_ans)
                    else 0)
            success[3] = success[3] + (1 if len(annealing_ans) ==
                    len(astar_ans) else 0)
            print(min(3, len(astar_ans) - len(astar_ans)))
            print(min(3, len(gbfs_ans) - len(astar_ans)))
            print(min(3, len(hc_ans) - len(astar_ans)))
            print(min(3, len(annealing_ans) - len(astar_ans)))
            res2[0]['Y'][max(0, min(3, len(astar_ans) - len(astar_ans)))][-1] += 1
            res2[1]['Y'][max(0, min(3, len(gbfs_ans) - len(astar_ans)))][-1] += 1
            res2[2]['Y'][max(0, min(3, len(hc_ans) - len(astar_ans)))][-1] += 1
            res2[3]['Y'][max(0, min(3, len(annealing_ans) - len(astar_ans)))][-1] += 1

        avg = [x / tries for x in avg]
        success = [x / tries * 100 for x in success]
        for i in range(len(avg)):
            res[i]['X'].append(p)
            res[i]['Y'].append(avg[i])
            res1[i]['X'].append(p)
            res1[i]['Y'].append(success[i])
            res2[i]['X'].append(p)
        success_rate.append(success)
        iterations.append(avg)
    #  plot_stacked_bar('Distance from best answer', 'P', '\\#',
    #          res2)
    #  plot_data('Test number of iterations by edge existance possibility',
    #          'P', 'Iterations',
    #          res)
    #  plot_data('Test success rate by edge existance possibility',
    #          'P', 'Success rate %',
    #          res1)
    plot_stacked_bar('Distance from best answer', 'P', '\\#',
            res2, 'TestByP')
    plot_data('Test number of iterations by edge existance possibility',
            'P', 'Iterations',
            res, 'TestByP')
    plot_data('Test success rate by edge existance possibility',
            'P', 'Success rate %',
            res1, 'TestByP')

def TestSuccessByRandStart(start=.04, end=0.5, diff=0.02, tries=15,
        p=0.2, nodes=20): # DOES NOT WORK
    """
    THIS DOES NOT FUNCTION I DON'T KNOW WHY I WROTE IT THIS WAY BUT UNLESS IT'S
    COMPLETELY REFACTORED, IT'S EITHER GOING TO RUN INCREDABLY SLOW OR JUST RETURN
    AN ERROR
    """
    success_rate = [] 
    iterations = []
    res = [GEN_SMP_DATA(), GEN_SMP_DATA(), GEN_SMP_DATA(),]
    res1 = [GEN_SMP_DATA(), GEN_SMP_DATA(), GEN_SMP_DATA(),]
    res2 = [GEN_SMP_DATA_STACKED(), GEN_SMP_DATA_STACKED(),
            GEN_SMP_DATA_STACKED(),]
    names = ['A*', 'Hill-climbing random start', 'Annealing random start',
            'Hill-climbing 0 start', 'Annealing 0 start']

    for i in range(len(res)):
        res[i]['name'] = names[i]
        res1[i]['name'] = names[i]
        res2[i]['name'] = names[i]
    
    for n in range(tries):
        g = gen_graph_eq_prob_edges(nodes=nodes, p=p)
        avg = [0, 0, 0]
        success = [0, 0, 0]
        astar_ans, astar_steps = AStar.Astar(g)
        for st in track(numpy.arange(start, end, diff)):
            for i in range(len(res2)):
                for t in res2[i]['Y']:
                    t.append(0)

            hc_ans, hc_steps = HillClimbing.hill_climbing(g, st)
            annealing_ans, annealing_steps = AnnealingSearch.annealing_search(g, st)

            avg[0] = avg[0] + astar_steps
            avg[1] = avg[1] + hc_steps
            avg[2] = avg[2] + annealing_steps

            success[0] = success[0] + (1 if len(astar_ans) ==
                    len(astar_ans)
                    else 0)
            success[1] = success[1] + (1 if len(hc_ans) == len(astar_ans)
                    else 0)
            success[2] = success[2] + (1 if len(annealing_ans) ==
                    len(astar_ans) else 0)
            res2[0]['Y'][max(0, min(3, len(astar_ans) - len(astar_ans)))][-1] += 1
            res2[1]['Y'][max(0, min(3, len(hc_ans) - len(astar_ans)))][-1] += 1
            res2[2]['Y'][max(0, min(3, len(annealing_ans) - len(astar_ans)))][-1] += 1

        avg = [x / tries for x in avg]
        success = [x / tries * 100 for x in success]
        success_rate.append(success)
        iterations.append(avg)
        for i in range(len(avg)):
            res[i]['X'].append(st)
            res[i]['Y'].append(avg[i])
            res1[i]['X'].append(st)
            res1[i]['Y'].append(success[i])
            res2[i]['X'].append(success[i])
    plot_stacked_bar('Distance from best answer', 
            'Possibilty of a node being in the start position', '\\#',
            res2, 'TestByRandomStart')
    plot_data('Test number of iterations', 
            'P', 'Iterations',
            res, 'TestByRandomStart')
    plot_data('Success rate by possibility of a node existing on start', 
            'P', 'Success rate %',
            res1, 'TestByRandomStart')


