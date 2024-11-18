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
    
    def enumerate_possible_moves(self, symbol, row, column, board, player):
        round1 = self.enumerate_possible_moves_helper(symbol, row, column, board, player)
        round1_possible_moves = round1[0]
        round1_locations = round1[1]
        final_list = []
        
        # goes through the possible moves from a "first round", uses the locations after the movement
        # is applied, and then adds all variations to the first round in a list
        for x in range(0, len(round1_possible_moves)):
            round2 = self.enumerate_possible_moves_helper(symbol,
                                                          round1_locations[x]["row"],
                                                          round1_locations[x]["column"],
                                                          round1_locations[x]["board"],
                                                          player, round1_possible_moves[x])
            round2_possible_moves = round2[0]            

            for y in range(0, len(round2_possible_moves)):
                final_list.append((round1_possible_moves[x], round2_possible_moves[y]))
            if len(round2_possible_moves) == 0:
                final_list.append((round1_possible_moves[x], None))
                
        # NOTICE: IN THE LIST OF POSSIBLE MOVES, IF A DIRECTION CANNOT LEAD TO ANY MORE FOLLOWING DIRECTIONS,
        # THAT DIRECTION AND NONE ARE ADDED TO THE LIST
        
        # if len(final_list) == 0:
        #     for x in range(0, len(round1_possible_moves)):
        #         final_list.append((round1_possible_moves[x], None))
                
        return final_list

    
    #Assumes the piece is a piece is a valid Piece object
    def enumerate_possible_moves_helper(self, symbol, row, column, board, player, prev_move = ""):
        print(symbol, row, column, board, player, prev_move)
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
        moves_round_one = [north({ "row" : row,"column" : column, "board" : board}), 
                           east({ "row" : row,"column" : column, "board" : board}), 
                           south({ "row" : row,"column" : column, "board" : board}), 
                           west({ "row" : row,"column" : column, "board" : board}), 
                           forward({ "row" : row,"column" : column, "board" : board}), 
                           backward({ "row" : row,"column" : column, "board" : board})]
        valid_moves = []
        new_locations = []
        
        for x in moves_round_one:
            x.execute()
            
            #immediately skips to the next iteration if piece is out of bounds
            if not (0 <= x.location["row"] < self.all_boards[0]._rows
                    and 0 <= x.location["column"] < self.all_boards[0]._columns
                    and 0 <= x.location["board"] < len(self.all_boards)):
                continue
            
            #checks to see if the location where the piece moved is occupied by not none
            if self.all_boards[x.location["board"]].occupied(x.location["row"], x.location["column"]) != None:
                chosen_piece = self.all_boards[x.location["board"]].occupied(x.location["row"], x.location["column"])
                #checks to see if the player does not own this piece, if so, continue to next iteration
                
                # if the piece has jumped boards and that space is not None, then it is not a viable move
                if board != x.location["board"]:
                    continue                
                #if player does own the piece and if the symbol in the moves square does not match the symbol of the original piece
                if player.owns_piece(chosen_piece.symbol) != None and chosen_piece.symbol != symbol:  
                    continue
                
            # checks to see if the player does not have any pieces in the case of a movement to the past
            if board == x.location["board"] + 1:
                extras = 0
                for piece in player._all_pieces:    
                    if piece.alive == True and piece.in_play == False:
                        extras += 1
                if prev_move == "b":
                    extras -= 1
                if extras <= 0:
                    continue
                    
            valid_moves.append(x.symbol)
            new_locations.append(x.location)

        return [valid_moves, new_locations]

        #TO DO : IMPLEMENT BETTER PIECES. MAYBE USE AN ITERATOR CLASS
    def better_pieces(self, player): 
        
        class PiecesIterable:
            def __init__(self, game, player):
                self.game = game
                self.player = player

            def __iter__(self):
                return PiecesIterator(self.game, self.player)

        class PiecesIterator:
            def __init__(self, game, player):
                self.game = game
                self.player = player

                self.index = 0

            def __next__(self):
                if self.index == len(self.player._all_pieces):
                    raise StopIteration()

                piece = self.player._all_pieces[self.index]
                self.index += 1 
                if piece.alive == True and piece.in_play == True and piece.location == self.player.focus:
                    possible_moves = self.game.enumerate_possible_moves(piece.symbol, piece.row, piece.column, piece.location, self.player)
                    if len(possible_moves) == 0:
                        return 0
                    if any(x[1] != None for x in possible_moves):
                        return 2
                    else:
                        return 1
                        
                        
                else:
                    return 0

            def __iter__(self):
                return self

        iterate_pieces = PiecesIterable(self, player)
        prelist = []
        for x in iterate_pieces:
            prelist.append(x)
        return max(prelist)
        
        


from player import Player    
if __name__ == "__main__":
    player1 = Player("white")
    player2 = Player("brown")
    game = Game(player1, player2)
    
    player1.focus= 2
    
    player1._all_pieces[0].alive = False
    player1._all_pieces[0].in_play = False
        
    player1._all_pieces[1].alive = True
    player1._all_pieces[1].in_play = False
    
    player1._all_pieces[2].row = 1
    player1._all_pieces[2].column = 0
    player1._all_pieces[2].location = 1
    player1._all_pieces[2].alive = True
    player1._all_pieces[2].in_play = True
    
    player1._all_pieces[3].row = 0
    player1._all_pieces[3].column = 1
    player1._all_pieces[3].location = 1
    player1._all_pieces[3].alive = True
    player1._all_pieces[3].in_play = True
    
    player1._all_pieces[4].row = 0
    player1._all_pieces[4].column = 1
    player1._all_pieces[4].location = 1
    player1._all_pieces[4].alive = True
    player1._all_pieces[4].in_play = True
        
    # player1._all_pieces[5].row = 1
    # player1._all_pieces[5].column = 0
    # player1._all_pieces[5].location = 2
    # player1._all_pieces[5].alive = True
    # player1._all_pieces[5].in_play = True
    player1._all_pieces[5].alive = False
    player1._all_pieces[5].in_play = False

    player1._all_pieces[6].row = 0
    player1._all_pieces[6].column = 0
    player1._all_pieces[6].location = 2
    player1._all_pieces[6].alive = True
    player1._all_pieces[6].in_play = True

    player2._all_pieces[6].row = 0
    player2._all_pieces[6].column = 1
    player2._all_pieces[6].location = 2
    player2._all_pieces[6].alive = True
    player2._all_pieces[6].in_play = True


    game.all_boards[1]._grid[1][0] = player1._all_pieces[2]
    game.all_boards[1]._grid[0][1] = player1._all_pieces[3]
    
    game.all_boards[2]._grid[0][1] = player1._all_pieces[4]
    # game.all_boards[2]._grid[1][0] = player1._all_pieces[5]
    game.all_boards[2]._grid[0][0] = player1._all_pieces[6]
    
    # game.all_boards[2]._grid[0][1] = player2._all_pieces[6]
    
    test = game.enumerate_possible_moves(player1._all_pieces[6].symbol,
                                        player1._all_pieces[6].row,
                                        player1._all_pieces[6].column,
                                        player1._all_pieces[6].location,
                                        player1)
       
    for x in test:
        print(x, '\n')
    game.show_game()
    
    print(game.better_pieces(player1))
    
    
        
        
"""PLAN

Isai: Work on enumerating all possible moves
+ Add validation checks to CLI 
+ Look into iterator pattern
+ Perhaps pick up where Teni left off with move + Perhaps pick up where Teni left off with move -  I think this would look like having CLI validation where if someone wants to move in a certain direction e.g. 
'e' we check that in our enumerated moves there exists a move with 'e' as the first thing in the tuple

Teni: Implement standard move
+ Command and decorators

"""