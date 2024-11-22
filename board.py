from piece import Piece

class Board(): 

    def __init__(self, rows = 4, columns = 4):
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
        if not self.occupied(row, column):
            self.grid[row][column] = piece
            piece.row = row            
            piece.column = column
            piece.in_play = True
            piece.location = board_id
            return True
        return False

    def remove_piece(self, row, column, piece):
        self.grid[row][column] = None
        piece.in_play = False
        piece.row = -1
        piece.column = -1
        piece.location = -1

    def kill_piece(self, row, column, piece):
        self.remove_piece(row, column, piece)
        piece.alive = False

    def occupied(self, row, column):
        return self.grid[row][column]
    
    def __repr__(self):
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