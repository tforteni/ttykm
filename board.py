from piece import Piece

class Board(): 

    def __init__(self, rows = 4, columns = 4):
        # class Grid():
        #     def __init__(self, rows, columns):
        #         self._grid = []
        #         for x in range(0, rows):
        #             self._grid.append([])
        #             for y in range(0, columns):
        #                 self._grid[x].append(None)
                        
        #     def __getitem__(self, row):
        #         return self._grid[row]

        #     def __setitem__(self, row, column, value):
        #         print ("A")
                
        self._rows = rows
        self._columns = columns 
        self._grid = []
            
        #Initialise grid to contain None in every space
        for x in range(0, self._columns):
            to_add = []
            for y in range(0, self._rows):
                to_add.append(None)
            self._grid.append(to_add)
            
    def add_piece(self, row, column, piece, board_id):
        if not self.occupied(row, column):
            self._grid[row][column] = piece
            piece.row = row            
            piece.column = column
            piece.in_play = True
            piece.location = board_id
            return True
        return False

    def remove_piece(self, row, column, piece):
        self._grid[row][column] = None
        piece.in_play = False
        piece.row = -1
        piece.column = -1
        piece.location = -1

    def kill_piece(self, row, column, piece):
        self.remove_piece(row, column)
        piece.alive = False
            
    # I'm using occupied_by instead
    # def space_empty(self, row, column): 
    #     return self._grid[row][column] == None

    def occupied(self, row, column):
        return self._grid[row][column]
    
    def swap_two_spaces(self, row1, column1, row2, column2):
        holder = self._grid[row1][column1]
        self._grid[row1][column1] = self._grid[row2][column2]
        self._grid[row2][column2] = holder
    
    def replace_space_with_another(self, row1, column1, row2, column2):
        self._grid[row2][column2] = self._grid[row1][column1]
        self._grid[row1][column1] = None

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
                if self._grid[x][y] == None:
                    str+= " "
                else:
                    str+= f"{self._grid[x][y]}"
                str+= "|"
            if x == self._rows-1:
                str += '\n' + spacer
        return str
    
    
# if __name__ == "__main__":
#     board = Board(4, 4)
#     board._grid[0][1] = "A"
#     print(board)
