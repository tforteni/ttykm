from board import Board

class Game:
    
    def __init__(self):
        self.all_boards = []
        for x in range(0, 3):
            new_board = Board(4,4)
            self.all_boards.append(new_board)
            
    def show_game(self):
        all_boards_repr = []
        str = ""
        
        for x in range(0, 3):
            new_board = self.all_boards[x]
            all_boards_repr.append(repr(new_board).splitlines())
                    
        for x in range(0, len(all_boards_repr[0])):
            if x != 0:
                str+= '\n'
            for y in range(0, len(all_boards_repr)):
                if y != 0:
                    str+= "   "
                str += all_boards_repr[y][x]            
        return str