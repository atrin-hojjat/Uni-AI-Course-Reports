import rich
import numpy as np
from rich.console import Console
from rich import box
from rich.table import Table
from rich.align import Align
from rich.live import Live
from rich.text import Text
from rich.prompt import IntPrompt
from engine.OthelloEngine import OthelloEngine, PLAYERS
from agent import AGENTS


class Game:
    def __init__(self):
        rich.print("Starting a new game")

        console = Console()
        self.boardSize = int(input("Enter board size(must be even): "))

        self.engine = OthelloEngine(self.boardSize)

        print(*[f"{i}. {AGENTS[i][0]}" for i in range(len(AGENTS))])
        fpa, spa = int(input("Select White's agent: ")), int(input("Select Black's agent: "))

        self.whiteAgent = AGENTS[fpa][1](PLAYERS.WHITE)
        self.blackAgent = AGENTS[spa][1](PLAYERS.BLACK)

        console.clear()

        with Live(self.drawTable(), console=console, screen=False,
                refresh_per_second=20) as live:
            while self.engine.getState()['gameEnded'] == False:
                player = ("Black" if self.engine.state['lastPlayer'] == 
                        PLAYERS.WHITE else "White")
                moveNo = None
                if self.engine.state['lastPlayer'] == PLAYERS.BLACK:
                    moveNo = self.whiteAgent.move(self.engine)
                else:
                    moveNo = self.blackAgent.move(self.engine)
                self.engine.makeMove(self.engine.getAvailableMoves()[moveNo])
                rich.print(self.engine.state)
                console.clear()
                live.update(self.drawTable())
        rich.print(self.engine.state)


                

    def drawTable(self) -> Table:
        grid = Table(show_header=False, show_footer=False)
        grid.box = box.SQUARE
        table = [[''] * self.boardSize for i in range(self.boardSize)]

        mp = self.engine.state['board']
        for x, y in np.ndindex((self.boardSize, self.boardSize)):
            if mp[x, y] == PLAYERS.BLACK:
                table[x][y] = 'B'
            elif mp[x, y] == PLAYERS.WHITE:
                table[x][y] = 'W'

        moves = self.engine.getAvailableMoves()
        print(moves)
        for ind in range(len(moves)):
            i, j = moves[ind]
            table[i][j] = str(ind)

        for row in table:
            grid.add_row(*row)

        return Align(grid, align="center")


