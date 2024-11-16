class Piece():

    def __init__(self, symbol, inplay = False, alive = False, board = -1):
        self._symbol = symbol
        self._in_play = False
        self._alive = False
        self._location = -1
        
    def __repr__(self):
        return self._symbol