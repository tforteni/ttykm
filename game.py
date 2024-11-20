import copy
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

    def is_over(self, player, other, print_it=True):
        eras = [0,0,0]
        eras[0] = len(player.copies_in_era(0))
        eras[1] = len(player.copies_in_era(1))
        eras[2] = len(player.copies_in_era(2))
        if eras.count(0) >= 2 and print_it:
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

        board_str += "black  \n"
        
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
        board_str += "white  "            
        print(board_str)
        
    def set_move_strategy(self, move_strategy):
        self._strategy = move_strategy

    def move_piece(self, piece, row, column, board_id, game, player, direction, leave_copy=False):
        # print("calling game move piece")
        board = self.all_boards[board_id]
        if direction in ["f", "b"]:
            game.set_move_strategy(TimeMove())
        elif board.occupied(row, column): #could add check for the kind of piece that occupies it
            game.set_move_strategy(PushMove())
        else: 
            game.set_move_strategy(Move())
        self._strategy.move(self, piece, row, column, board, player, direction, leave_copy)
    
    def enumerate_possible_moves(self, this_piece, symbol, row, column, board, player, other):
        # print(f"HERE IS ALL: {self.player1.all_pieces}")
        round1 = self.enumerate_possible_moves_helper(this_piece, symbol, row, column, board, player, other)
        round1_possible_moves = round1[0]
        round1_locations = round1[1]
        final_list = []
        final_move_values = []
        
        # goes through the possible moves from a "first round", uses the locations after the movement
        # is applied, and then adds all variations to the first round in a list
        for x in range(0, len(round1_possible_moves)):
            round2 = self.enumerate_possible_moves_helper(this_piece, symbol,
                                                          round1_locations[x]["row"],
                                                          round1_locations[x]["column"],
                                                          round1_locations[x]["board"],
                                                          player, other, round1_possible_moves[x])
            round2_possible_moves = round2[0]
            round2_locations = round2[1]          

            for y in range(0, len(round2_possible_moves)):
                final_list.append((round1_possible_moves[x], round2_possible_moves[y]))
                # print(f"\n{(round1_possible_moves[x], round2_possible_moves[y])}")
                # print(f"\n{(round1_locations[x]["row"], round1_locations[x]["column"])}")
                old_game = copy.deepcopy(self)
                piece_copy = copy.deepcopy(this_piece)
                player_copy = copy.deepcopy(player)
                player_copy.all_pieces[player.all_pieces.index(this_piece)] = piece_copy
                val1 = old_game.move_piece_copy(piece_copy, round1_locations[x]["row"], round1_locations[x]["column"], round1_locations[x]["board"], self, player_copy, round1_possible_moves[x])
                game_over = 0
                if (player_copy == old_game.player1):
                    if old_game.is_over(player_copy, old_game.player2, False):
                        print(1)
                        # sys.exit(0)
                        game_over = 9999
                elif old_game.is_over(player_copy, old_game.player1, False):
                    print(2)
                    # sys.exit(0)
                    game_over = -9999
                val2 = old_game.move_piece_copy(piece_copy, round2_locations[y]["row"], round2_locations[y]["column"], round2_locations[y]["board"], self, player_copy, round2_possible_moves[y])
                game_over2 = 0
                if (player_copy == old_game.player1):
                    if old_game.is_over(player_copy, old_game.player2, False):
                        print(3)
                        # sys.exit(0)
                        game_over2 = 9999
                elif old_game.is_over(player_copy, old_game.player1, False):
                    print(4)
                    # sys.exit(0)
                    game_over2 = -9999
                final_move_values.append(val1 + val2 + game_over + game_over2)
            if len(round2_possible_moves) == 0:
                final_list.append((round1_possible_moves[x], None))
                old_game = copy.deepcopy(self)
                piece_copy = copy.deepcopy(this_piece)
                val1 = old_game.move_piece_copy(piece_copy, round1_locations[x]["row"], round1_locations[x]["column"], round1_locations[x]["board"], self, player, round1_possible_moves[x])
                final_move_values.append(val1)
                
        # NOTICE: IN THE LIST OF POSSIBLE MOVES, IF A DIRECTION CANNOT LEAD TO ANY MORE FOLLOWING DIRECTIONS,
        # THAT DIRECTION AND NONE ARE ADDED TO THE LIST
        
        # if len(final_list) == 0:
        #     for x in range(0, len(round1_possible_moves)):
        #         final_list.append((round1_possible_moves[x], None))
        
        if not final_list and not final_move_values:
            return []
        return [final_list, final_move_values]

    
    #Assumes the piece is a piece is a valid Piece object
    def enumerate_possible_moves_helper(self, this_piece, symbol, row, column, board, player, other, prev_move = ""):
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
        # move_values = []
        
        for x in moves_round_one:
            x.execute()
            
            #immediately skips to the next iteration if piece is out of bounds
            if not (0 <= x.location["row"] < self.all_boards[0]._rows
                    and 0 <= x.location["column"] < self.all_boards[0]._columns
                    and 0 <= x.location["board"] < len(self.all_boards)):
                continue
            
            if prev_move == "b" and x.symbol == "f":
                continue
            #checks to see if the location where the piece moved is occupied by not none
            if self.all_boards[x.location["board"]].occupied(x.location["row"], x.location["column"]) != None:
                chosen_piece = self.all_boards[x.location["board"]].occupied(x.location["row"], x.location["column"])
                #checks to see if the player does not own this piece, if so, continue to next iteration
                
                # if the piece has jumped boards and that space is not None, then it is not a viable move
                # 2nd and 3rd checks are in the case of a forward backward jump

                if board != x.location["board"] and prev_move != "f" and x.symbol != "b":
                    continue
                #if player does own the piece and if the symbol in the moves square does not match the symbol of the original piece
                if player.owns_piece(chosen_piece.symbol) != None and chosen_piece.symbol != symbol:
                    if any(y.row == row and y.column == column and y.location == board and y.alive == True and y.in_play == True for y in other.all_pieces) and x.symbol == prev_move:
                        ""
                    else:
                        continue
                
            # checks to see if the player does not have any pieces in the case of a movement to the past
            if board == x.location["board"] + 1:
                extras = 0
                for piece in player.all_pieces:    
                    if piece.alive == True and piece.in_play == False:
                        extras += 1
                if prev_move == "b":
                    extras -= 1
                if extras <= 0:
                    continue
                    
            valid_moves.append(x.symbol)
            new_locations.append(x.location)

        return [valid_moves, new_locations]#, move_values]

    def move_piece_copy(self, piece, row, column, board_id, game, player, direction, leave_copy=False):
        board = self.all_boards[board_id]
        if direction in ["f", "b"]:
            self.set_move_strategy(TimeMove())
        elif board.occupied(row, column): #could add check for the kind of piece that occupies it
            self.set_move_strategy(PushMove())
        else: 
            self.set_move_strategy(Move())
        self._strategy.move(self, piece, row, column, board, player, direction, leave_copy)
        if player == self.player1:
            return player.calculate_values(self.player2)
        else:
            return player.calculate_values(self.player1) #changed all instances of old_game to self since i am calling this method on old_game.


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
                if self.index == len(self.player.all_pieces):
                    raise StopIteration()

                piece = self.player.all_pieces[self.index]
                if self.player == self.game.player1:
                    other = self.game.player2
                else:
                    other = self.game.player1
                self.index += 1 
                if piece.alive == True and piece.in_play == True and piece.location == self.player.focus:
                    possible_moves = self.game.enumerate_possible_moves(piece, piece.symbol, piece.row, piece.column, piece.location, self.player, other)
                    if len(possible_moves) == 0:
                        return 0
                    if any(len(x) > 1 and x[1] != None for x in possible_moves):
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
    
    def fill_empty_board(self):
        new_all_boards = []
        for x in range(0, 3):
            new_board = Board(4,4)
            new_all_boards.append(new_board)
        
        for x in self.player1.all_pieces:
            if x.row != -1 or x.column != -1 or x.location != -1:
                new_all_boards[x.location].grid[x.row][x.column] = x
        for x in self.player2.all_pieces:
            if x.row != -1 or x.column != -1 or x.location != -1:
                new_all_boards[x.location].grid[x.row][x.column] = x
        return new_all_boards