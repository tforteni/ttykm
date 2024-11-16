from piece import Piece

class CheckerBoard(): 

    def __init__(self, rows = 4, columns = 4):
        self._rows = rows
        self._columns = columns 
        self._board = []
        
        for x in range(0, self._columns):
            to_add = []
            for y in range(0, self._rows):
                to_add.append(None)
            self._board.append(to_add)
            
    def space_empty(self, column, row):
        return self._board[column][row] == None
    
    def swap_two_spaces(self, column1, row1, row2, column2):
        holder = self._board[column1][row1]
        self._board[column1][row1] = self._board[column2][row2]
        self._board[column2][row2] = holder
    
    def replace_space_with_another(self, column1, row1, row2, column2):
        self._board[column2][row2] = self._board[column1][row1]
        self._board[column1][row1] = None
        
    def remove_space(self, column1, row1):
        self._board[column1][row1] = None

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
                if self._board[x][y] == None:
                    str+= " "
                else:
                    str+= f"{self._board[x][y]}"
                str+= "|"
            if x == self._columns-1:
                str += '\n' + spacer
        return str
    
if __name__ == "__main__":
    piece1 = Piece("A")
    piece2 = Piece("B")
    piece3 = Piece("X")
    piece4 = Piece(";")
    test = CheckerBoard(4, 4)
    test._board[0][2] = "A"
    test._board[1][2] = "B"
    test._board[2][2] = "C"
    test._board[3][3] = "D"
    
    print(test)
    test.swap_two_spaces(0,2,1,2)
