from . import Agent
from rich.prompt import IntPrompt
from engine.OthelloEngine import PLAYERS
import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
#  from MiniMax.MiniMax import calculateMiniMax
from MiniMax import calculateMiniMax


#  aiDll = ctypes.CDLL("./agent/MiniMaxCompEng/calc_minimax_eng")

#  aiDll.calc.restype = ctypes.c_int


class MiniMaxAgent(Agent.AbstractAgent):
    depth = 7
    def __init__(self, color, depth=7):
        self.color = color
        self.colorName = "Black" if PLAYERS.BLACK == color else "White"
        self.depth = depth

    #  def move(self, engine):
    #      #  grid = np.array(engine.state['board'], dtype=np.int)
    #      grid = np.copy(engine.state['board'].astype(np.int32))
    #      N = engine.boardSize
    #      _p = ndpointer(dtype=np.int32, ndim=2, shape=(N, N), flags='C')

    #      aiDll.calc.argtypes = [ctypes.c_int, _p, ctypes.c_int,
    #              ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
    #              ctypes.c_int]
    #      i, j = ctypes.c_int(), ctypes.c_int()
    #      bestOutcome = aiDll.calc(ctypes.c_int(N), grid, ctypes.c_int(self.color),
    #              ctypes.byref(i), ctypes.byref(j), ctypes.c_int(self.depth))


    #      return engine.getAvailableMoves().index((i.value, j.value))


    def move(self, engine):
        grid = np.copy(engine.state['board'].astype(np.int32))
        N = engine.boardSize

        #  print(grid, grid.tolist())
        #  result = calculateMiniMax(N, grid.tolist(), self.color, self.depth)
        result = calculateMiniMax(N, grid, self.color,
                self.depth)

        return engine.getAvailableMoves().index(result['move'])
        
