from board import Board

class Game:
    
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.all_boards = []
        for x in range(0, 3):
            new_board = Board(4,4)
            self.all_boards.append(new_board)

    def build_game(self): 
        #TO DO: sets up initial game config
        for board in self.all_boards:
            piece = self.player1.get_next_piece()
            board.add_piece(0,0,piece)
            piece = self.player2.get_next_piece()
            board.add_piece(3,3,piece)
            
    def show_game(self):
        all_boards_repr = []
        board_str = "---------------------------------\n"
        board_str += "                          black\n"
        
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
        board_str += "\n  white"            
        print(board_str)