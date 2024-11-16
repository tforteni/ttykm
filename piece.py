class Piece():

    def __init__(self, symbol, inplay = False, alive = True, board = -1):
        self._symbol = symbol
        self._in_play = inplay
        self._alive = alive
        self._location = board
        
    def __repr__(self):
        return self._symbol