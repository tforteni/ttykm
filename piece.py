class Piece():

    def __init__(self, symbol):
        if type(symbol) == str and len(symbol) == 1:
            self._symbol = symbol
        else:
            self._symbol = "E" # "E" for Error
            
            
        
    def __repr__(self):
        return self._symbol