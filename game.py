from board import Board

class Game:
    
    def __init__(self):
        self.all_boards = []
        
        #initializes Game object with 3 boards
        for x in range(0, 3):
            new_board = Board(4,4)
            self.all_boards.append(new_board)

    def build_game(self): 
        #TO DO: sets up initial game config
        pass
            
    def show_game(self):
        all_boards_repr = []
        board_str = ""
        
        for x in range(0, 3):
            new_board = self.all_boards[x]
            all_boards_repr.append(repr(new_board).splitlines())
                    
        for x in range(0, len(all_boards_repr[0])):
            if x != 0:
                board_str+= '\n'
            for y in range(0, len(all_boards_repr)):
                if y != 0:
                    board_str+= "   "
                board_str += all_boards_repr[y][x]            
        print(board_str)