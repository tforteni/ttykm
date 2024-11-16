from piece import Piece

class Board(): 

    def __init__(self, rows = 4, columns = 4):
        self._rows = rows
        self._columns = columns 
        self._grid = []
        
        #Initialise grid to contain None in every space
        for x in range(0, self._columns):
            to_add = []
            for y in range(0, self._rows):
                to_add.append(None)
            self._grid.append(to_add)

    def add_piece(self, column, row, piece):
        if self.space_empty(column, row):
            self._grid[column][row] = piece
            piece.in_play = True
            return True
        return False
            
    def space_empty(self, column, row):
        return self._grid[column][row] == None
    
    def swap_two_spaces(self, column1, row1, row2, column2):
        holder = self._grid[column1][row1]
        self._grid[column1][row1] = self._grid[column2][row2]
        self._grid[column2][row2] = holder
    
    def replace_space_with_another(self, column1, row1, row2, column2):
        self._grid[column2][row2] = self._grid[column1][row1]
        self._grid[column1][row1] = None
        
    def remove_space(self, column1, row1):
        self._grid[column1][row1] = None

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
            
        for x in range(0, self._columns):
            if x != 0:
                str += '\n'
            str += spacer
            for y in range(0, self._rows):
                if y == 0:
                    str += "\n" + "|" 
                if self._grid[x][y] == None:
                    str+= " "
                else:
                    str+= f"{self._grid[x][y]}"
                str+= "|"
            if x == self._columns-1:
                str += '\n' + spacer
        return str