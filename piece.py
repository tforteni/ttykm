class Piece():

    def __init__(self, symbol, inplay = False, alive = False, board = -1):
        self.symbol = symbol
        self.in_play = inplay
        self.alive = alive
        self.location = board
        
    def __repr__(self):
        return self.symbol