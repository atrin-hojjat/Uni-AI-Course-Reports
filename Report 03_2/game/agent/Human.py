from . import Agent
from rich.prompt import IntPrompt
from engine.OthelloEngine import PLAYERS

class HumanAgent(Agent.AbstractAgent):
    def __init__(self, color):
        self.color = color
        self.colorName = "Black" if PLAYERS.BLACK == color else "White"

    def move(self, engine):
        moveNo = IntPrompt.ask(f"{self.colorName} to move")
        return moveNo


