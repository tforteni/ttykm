from piece import Piece

class Board(): 
    '''
    An object that represents a game board represented through a row priority grid. Spaces are able to hold objects.
    '''

    def __init__(self, rows = 4, columns = 4):
        '''
        Initializes a Board object with the amount of rows, columns, and the respective grid 
        where all [row][column] locations are set to None
        '''
        self._rows = rows
        self._columns = columns 
        self.grid = []
            
        #Initialise grid to contain None in every space
        for x in range(0, self._columns):
            to_add = []
            for y in range(0, self._rows):
                to_add.append(None)
            self.grid.append(to_add)
            
    def add_piece(self, row, column, piece, board_id):
        '''
        If a board's grid location is not occupied, the provided Piece will be added to that location.
        It's in_play variable is set to true, it is now considered part of the game.  
        '''
        if not self.occupied(row, column):
            self.grid[row][column] = piece
            piece.row = row            
            piece.column = column
            piece.in_play = True
            piece.location = board_id
            return True
        return False

    def remove_piece(self, row, column, piece):
        '''
        Removes a Piece from the board's grid. It's "in_play" value is set to false, 
        and it's row, column, and location variables are all set to -1. 
        '''
        self.grid[row][column] = None
        piece.in_play = False
        piece.row = -1
        piece.column = -1
        piece.location = -1

    def kill_piece(self, row, column, piece):
        '''
        Removes a Piece from the the game. It's "alive" variable is set to False. 
        Utilizes remove_piece to properly handle the other variables. 
        '''
        self.remove_piece(row, column, piece)
        piece.alive = False

    def occupied(self, row, column):
        '''
        Returns the item inn a specific location [row][column] on the board's grid.
        It either returns a Piece object or None
        '''
        return self.grid[row][column]
    
    def __repr__(self):
        '''
        Creates a string to print the board and its objects. 
        '''
        str = ""
        spacer = ""
        dict = {
            0 : "-",
            1 : "+",
        }
        for y in range(0, self._rows):
            if y == 0:
                spacer += dict[1]
            spacer+= dict[0]
            spacer+= dict[1]
            
        for x in range(0, self._rows):
            if x != 0:
                str += '\n'
            str += spacer
            for y in range(0, self._columns):
                if y == 0:
                    str += "\n" + "|" 
                if self.grid[y][x] == None:
                    str+= " "
                else:
                    str+= f"{self.grid[y][x]}"
                str+= "|"
            if x == self._rows-1:
                str += '\n' + spacer
        return str