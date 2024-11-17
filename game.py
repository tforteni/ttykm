from board import Board
from movestrategy import Move, PushMove, TimeMove

class Game:
    
    def __init__(self, player1, player2, move_strategy=Move()):
        self.player1 = player1
        self.player2 = player2
        self.all_boards = []
        self._strategy = move_strategy
        
        #initializes Game object with 3 boards
        for x in range(0, 3):
            new_board = Board(4,4)
            self.all_boards.append(new_board)

    def build_game(self): 
        #Sets up initial game config
        for index, board in enumerate(self.all_boards):
            piece = self.player1.get_next_piece()
            board.add_piece(3,3,piece, index)
            piece = self.player2.get_next_piece()
            board.add_piece(0,0,piece, index)
            
    def show_game(self):
        all_boards_repr = []
        board_str = "---------------------------------\n"
        if self.player2.focus == 0:
            board_str += "  "
        elif self.player2.focus == 1:
            board_str += "              "
        elif self.player2.focus == 2:
            board_str += "                          "

        board_str += "black\n"
        
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
        if self.player1.focus == 0:
            board_str += "\n  "
        elif self.player1.focus == 1:
            board_str += "\n              "
        elif self.player1.focus == 2:
            board_str += "\n                          "
        board_str += "white"            
        print(board_str)
        
    def set_move_strategy(self, move_strategy):
        self._strategy = move_strategy

    def move_piece(self, piece, row, column, board_id, game, player, direction, leave_copy=False): #TO DO:Implement standard move with command/decorators for if we're pushing/paradoxing etc
        print("calling game move piece\n")
        board = self.all_boards[board_id]
        if direction in ["f", "b"]:
            game.set_move_strategy(TimeMove())
        elif board.occupied(row, column): #could add check for the kind of piece that occupies it
            game.set_move_strategy(PushMove())
        else: 
            game.set_move_strategy(Move())
        self._strategy.move(self, piece, row, column, board, player, direction, leave_copy)
    
    def enumerate_possible_moves(self, piece):
        possible_moves =  []
        moves_dictionary =  ["n", "s", "e", "w", "b", "f"]
        
        row= piece.row
        column = piece.column
        
                
        
        
"""PLAN

Isai: Work on enumerating all possible moves
+ Add validation checks to CLI 
+ Look into iterator pattern
+ Perhaps pick up where Teni left off with move

Teni: Implement standard move
+ Command and decorators

"""