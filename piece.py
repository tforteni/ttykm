class Piece():

    def __init__(self, symbol, inplay = False, alive = True, location = -1, row = -1, column = -1):
        self.symbol = symbol
        self.in_play = inplay
        self.alive = alive
        self.location = location
        self.row = row
        self.column = column
        
    def __repr__(self):
        return self.symbol