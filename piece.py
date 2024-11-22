class Piece():
    '''
    An object that represents a piece, dead, in play, or useable, for a game. 
    They are placed on the squares of a Board
    '''
    def __init__(self, symbol, inplay = False, alive = True, location = -1, row = -1, column = -1):
        '''
        Initializes a Piece object. Default arguments indicate that a piece is alive but not in current play.
        '''
        self.symbol = symbol
        self.in_play = inplay
        self.alive = alive
        self.location = location
        self.row = row
        self.column = column
        
    def __repr__(self):
        '''
        Represents a Piece by its symbol
        '''
        return self.symbol