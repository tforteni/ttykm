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

    def is_over(self, player, other):
        eras = [0,0,0]
        eras[0] = len(player.copies_in_era(0))
        eras[1] = len(player.copies_in_era(1))
        eras[2] = len(player.copies_in_era(2))
        if eras.count(0) >= 2:
            print(f"{other.id} has won")
            return True
        return False

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

    def move_piece(self, piece, row, column, board_id, game, player, direction, leave_copy=False):
        print("calling game move piece\n")
        board = self.all_boards[board_id]
        if direction in ["f", "b"]:
            game.set_move_strategy(TimeMove())
        elif board.occupied(row, column): #could add check for the kind of piece that occupies it
            game.set_move_strategy(PushMove())
        else: 
            game.set_move_strategy(Move())
        self._strategy.move(self, piece, row, column, board, player, direction, leave_copy)
    
    def enumerate_possible_moves(self, column, row, board, player):
        round1 = self.enumerate_possible_moves_helper(column, row, board, player)
        round1_possible_moves = round1[0]
        round1_locations = round1[1]
        final_list = []
        
        # goes through the possible moves from a "first round", uses the locations after the movement
        # is applied, and then adds all variations to the first round in a list
        for x in range(0, len(round1_possible_moves)):
            round2 = self.enumerate_possible_moves_helper(round1_locations[x]["column"],
                                                          round1_locations[x]["row"],
                                                          round1_locations[x]["board"],
                                                          player)
            round2_possible_moves = round2[0]            

            for y in range(0, len(round2_possible_moves)):
                final_list.append((round1_possible_moves[x], round2_possible_moves[y]))
                
        # if there are no viable second moves, then the solo moves are added as a pair with None
        if len(final_list) == 0:
            for x in range(0, len(round1_possible_moves)):
                final_list.append((round1_possible_moves[x], None))
                
        return final_list

    
    #Assumes the piece is a piece is a valid Piece object
    def enumerate_possible_moves_helper(self, column, row, board, player):
        class AbstractCommand:
            def execute(self):
                raise NotImplemented()

        class north(AbstractCommand):
            def __init__(self, location):
                self.location = location
                self.symbol = "n"
            def execute(self):
                self.location["column"] = self.location["column"] - 1 
                
        class east(AbstractCommand):
            def __init__(self, location):
                self.location = location
                self.symbol = "e"
            def execute(self):
                self.location["row"] = self.location["row"] + 1 
                
        class south(AbstractCommand):
            def __init__(self, location):
                self.location = location
                self.symbol = "s"
            def execute(self):
                self.location["column"] = self.location["column"] + 1 
        
        class west(AbstractCommand):
            def __init__(self, location):
                self.location = location
                self.symbol = "w"
            def execute(self):
                self.location["row"] = self.location["row"] - 1 
                
        class forward(AbstractCommand):
            def __init__(self, location):
                self.location = location
                self.symbol = "f"
            def execute(self):
                self.location["board"] = self.location["board"] + 1 

        class backward(AbstractCommand):
            def __init__(self, location):
                self.location = location
                self.symbol = "b"
            def execute(self):
                self.location["board"] = self.location["board"] - 1 
        
        
        # location =  {"column" : piece.column, "row" : piece.row, "board" : piece.location}
        moves_round_one = [north({"column" : column, "row" : row, "board" : board}), 
                           east({"column" : column, "row" : row, "board" : board}), 
                           south({"column" : column, "row" : row, "board" : board}), 
                           west({"column" : column, "row" : row, "board" : board}), 
                           forward({"column" : column, "row" : row, "board" : board}), 
                           backward({"column" : column, "row" : row, "board" : board})]
        valid_moves = []
        new_locations = []

        
        for x in moves_round_one:
            x.execute()
            
            #immediately skips to the next iteration if piece is out of bounds
            if not (0 <= x.location["column"] < self.all_boards[0]._columns
                    and 0 <= x.location["row"] < self.all_boards[0]._rows
                    and 0 <= x.location["board"] < len(self.all_boards)):
                continue
            #checks to see if the location where the piece moved is occupied by not none
            if self.all_boards[x.location["board"]].occupied(x.location["row"], x.location["column"]) != None:
                #checks to see if the player does not own this piece, if so, continue to next iteration
                if player.owns_piece(self.all_boards[x.location["board"]].occupied(x.location["row"], x.location["column"])) == None:
                    continue
                # if the piece has jumped boards and that space is not None, then it is not a viable move
                if board != x.location["board"]:
                    continue
            valid_moves.append(x.symbol)
            new_locations.append(x.location)

        return [valid_moves, new_locations]

from player import Player    
if __name__ == "__main__":
    player1 = Player("white")
    
    player1._all_pieces[0].row = 1
    player1._all_pieces[0].column = 0
    player1._all_pieces[0].location = 1
        
    player1._all_pieces[1].row = 1
    player1._all_pieces[1].column = 0
    player1._all_pieces[1].location = 1
    
    
    player1._all_pieces[4].row = 0
    player1._all_pieces[4].column = 1
    player1._all_pieces[4].location = 2
    
    
    player1._all_pieces[5].row = 1
    player1._all_pieces[5].column = 0
    player1._all_pieces[5].location = 2
    

    
    player1._all_pieces[6].row = 0
    player1._all_pieces[6].column = 0
    player1._all_pieces[6].location = 2
    player2 = Player("brown")
    game = Game(player1, player2)
    
    game.all_boards[2]._grid[1][0] = player1._all_pieces[5]
    game.all_boards[2]._grid[0][1] = player1._all_pieces[4]
    game.all_boards[2]._grid[0][0] = player1._all_pieces[6]
    game.all_boards[1]._grid[1][0] = player1._all_pieces[0]
    game.all_boards[1]._grid[0][1] = player1._all_pieces[1]


    
    test = game.enumerate_possible_moves(player1._all_pieces[6].column,
                                        player1._all_pieces[6].row,
                                        player1._all_pieces[6].location,
                                        player1)
    
    for x in test:
        print(x, '\n')
    game.show_game()
        
        
"""PLAN

Isai: Work on enumerating all possible moves
+ Add validation checks to CLI 
+ Look into iterator pattern
+ Perhaps pick up where Teni left off with move + Perhaps pick up where Teni left off with move -  I think this would look like having CLI validation where if someone wants to move in a certain direction e.g. 
'e' we check that in our enumerated moves there exists a move with 'e' as the first thing in the tuple

Teni: Implement standard move
+ Command and decorators

"""