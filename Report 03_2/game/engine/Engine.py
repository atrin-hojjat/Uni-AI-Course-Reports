

class AbstractEngine:

    def __init__(self):
        self.state = {}
        self.history = []


    def getHistory(self):
        return self.history
    def getState(self):
        return self.state

    def getAvailableMoves(self):
        pass

    def makeMove(self, move):
        pass
    
    def loadGame(game):
        pass
