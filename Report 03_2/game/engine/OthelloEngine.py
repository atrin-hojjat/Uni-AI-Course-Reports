from . import Engine
import enum
import numpy as np
import rich

class PLAYERS:
    NONE = 0
    BLACK = 1
    WHITE = 2

class OthelloEngine(Engine.AbstractEngine):
    def __init__(self, boardSize):
        self.boardSize = boardSize
        assert(boardSize % 2 == 0)
        self.state = {'lastPlayer': PLAYERS.BLACK, 'board': np.zeros((boardSize,
            boardSize)), 'score': {'black': 2, 'white': 2}, 'gameEnded': False}
        for i in range(int((boardSize - 2) / 2), int(boardSize / 2 + 1)):
            for j in range(int((boardSize - 2) / 2), int(boardSize / 2 + 1)):
                self.state['board'][i][j] = (
                        PLAYERS.WHITE if (i + j) % 2 == 0 else PLAYERS.BLACK)
        self.availableMoves = None
        self.history = []
        self.getAvailableMoves()


    def getAvailableMoves(self):
        if self.availableMoves:
            return [tuple(i) for i in self.availableMoves]
        curPlayer = (PLAYERS.BLACK if 
                self.state['lastPlayer'] == PLAYERS.WHITE else PLAYERS.WHITE)
        availableMoves = []
        
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.state['board'][i][j] != PLAYERS.NONE:
                    continue
                # Horizontal
                ok = False
                for jp in range(j + 1, self.boardSize):
                    if self.state['board'][i][jp] == PLAYERS.NONE:
                        break
                    elif self.state['board'][i][jp] == curPlayer:
                        ok = jp > j + 1
                        break

                if ok:
                    availableMoves.append((i, j))
                    continue
                for jp in range(j - 1, -1, -1):
                    if self.state['board'][i][jp] == PLAYERS.NONE:
                        break
                    elif self.state['board'][i][jp] == curPlayer:
                        ok = jp < j - 1
                        break
                if ok:
                    availableMoves.append((i, j))
                    continue


                # Vertical
                for ip in range(i + 1, self.boardSize):
                    if self.state['board'][ip][j] == PLAYERS.NONE:
                        break
                    elif self.state['board'][ip][j] == curPlayer:
                        ok = ip > i + 1
                        break
                if ok:
                    availableMoves.append((i, j))
                    continue
                for ip in range(i - 1, -1, -1):
                    if self.state['board'][ip][j] == PLAYERS.NONE:
                        break
                    elif self.state['board'][ip][j] == curPlayer:
                        ok = ip < i - 1
                        break
                if ok:
                    availableMoves.append((i, j))
                    continue

                # Diagonal
                for idel in range(-1, 2, 2):
                    for jdel in range(-1, 2, 2):
                        for k in range(1, self.boardSize):
                            if i + idel * k >= self.boardSize or i + idel * k < 0:
                                break
                            if j + jdel * k >= self.boardSize or j + jdel * k < 0:
                                break
                            ip, jp = i + idel * k, j + jdel * k
                            if self.state['board'][ip][jp] == PLAYERS.NONE:
                                break
                            elif self.state['board'][ip][jp] == curPlayer:
                                ok = k > 1
                                break
                        if ok: break
                if ok:
                    availableMoves.append((i, j))
                    continue

        self.availableMoves = [tuple(i) for i in availableMoves]
        return availableMoves

    def makeMove(self, move):
        if self.state['gameEnded']:
            return False
        if move not in self.availableMoves:
            return False
        self.history.append({'move': move, 'board': self.state['board']})
        board = np.copy(self.state['board'])
        self.state['board'] = board
        curPlayer = (PLAYERS.BLACK if 
                self.state['lastPlayer'] == PLAYERS.WHITE else PLAYERS.WHITE)
        self.state['lastPlayer'] = curPlayer

        i, j = move
        board[i][j] = curPlayer
        for jp in range(j + 1, self.boardSize):
            if self.state['board'][i][jp] == PLAYERS.NONE:
                break
            elif self.state['board'][i][jp] == curPlayer:
                for t in range(j + 1, jp):
                    self.state['board'][i][t] = curPlayer
                break

        for jp in range(j - 1, -1, -1):
            if self.state['board'][i][jp] == PLAYERS.NONE:
                break
            elif self.state['board'][i][jp] == curPlayer:
                for t in range(j - 1, jp, -1):
                    self.state['board'][i][t] = curPlayer
                break


        # Vertical
        for ip in range(i + 1, self.boardSize):
            if self.state['board'][ip][j] == PLAYERS.NONE:
                break
            elif self.state['board'][ip][j] == curPlayer:
                for t in range(i + 1, ip):
                    self.state['board'][t][j] = curPlayer
                break
        for ip in range(i - 1, -1, -1):
            if self.state['board'][ip][j] == PLAYERS.NONE:
                break
            elif self.state['board'][ip][j] == curPlayer:
                for t in range(i - 1, ip, -1):
                    self.state['board'][t][j] = curPlayer
                ok = ip < i - 1
                break

        # Diagonal
        for idel in range(-1, 2, 2):
            for jdel in range(-1, 2, 2):
                for k in range(1, self.boardSize):
                    if i + idel * k >= self.boardSize or i + idel * k < 0:
                        break
                    if j + jdel * k >= self.boardSize or j + jdel * k < 0:
                        break
                    ip, jp = i + idel * k, j + jdel * k
                    if self.state['board'][ip][jp] == PLAYERS.NONE:
                        break
                    elif self.state['board'][ip][jp] == curPlayer:
                        for kp in range(1, k):
                            self.state['board'][i + idel * kp][j + jdel * kp] = curPlayer
                        break
        self.availableMoves = None
        t = self.getAvailableMoves()
        
        ongoing = False
        blackScore, whiteScore = 0, 0
        for ix, iy in np.ndindex((self.boardSize, self.boardSize)):
            if self.state['board'][ix, iy] == PLAYERS.NONE:
                ongoing = True
            elif self.state['board'][ix, iy] == PLAYERS.WHITE:
                whiteScore = whiteScore + 1
            elif self.state['board'][ix, iy] == PLAYERS.BLACK:
                blackScore = blackScore + 1
        self.state['score']['black'], self.state['score']['white'] = blackScore, whiteScore
        if not ongoing:
            self.state['gameEnded'] = True

        if ongoing and len(t) == 0:
            # Skip One Move
            curPlayer = (PLAYERS.BLACK if 
                    self.state['lastPlayer'] == PLAYERS.WHITE else PLAYERS.WHITE)

            self.history.append({'move': None, 'board': np.copy(self.state['board'])})
            self.state['lastPlayer'] = curPlayer

        return True



