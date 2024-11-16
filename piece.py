class Piece():

    def __init__(self, symbol, inplay = False, alive = True, board = -1):
        self.symbol = symbol
        self.in_play = inplay
        self.alive = alive
        self.location = -1
        
    def __repr__(self):
        return self._symbol