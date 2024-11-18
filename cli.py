import sys
from game import Game
from player import Player

class CLI:
    """Display the CLI menu and respond to choices when run."""

    def __init__(self, player1, player2, history, display):
        self._selected_account = None
        self.player1 = Player("white", player1)
        self.player2 = Player("black", player2)
        self._game = Game(self.player1, self.player2)
        self._turns = 1
        self._state = Player1State(self, self.player1)
        self._history = history
        if self._history == "on":
            self._save_states = SaveStates()
        self._display = display

    def set_state(self, new_state):
        """Sets the current state(player)."""
        self._state = new_state

    def run(self):
        """Display the game and menu and respond to choices."""
        self._game.build_game()
        while not self._game.is_over(self._state.player, self._state.other):
            self._game.show_game()
            #TO DO: Advanced error checking
            print(f"Turn: {self._turns}, Current player: {self._state.player.id}")
            
            #Gives a number from 0, 1, and 2. The max number of moves all pieces are able to move.
            #0- all pieces cannot move at all
            #1- at least one piece can move once
            #2- at least one piece can move twice
            all_player_pieces = self._game.better_pieces(self._state.player)
            if not self._state.player.copies_in_era(self._state.player.focus) or all_player_pieces == 0:
                print("No copies to move")
                copy = None
                move1 = None
                move2 = None
            else:
                while True:
                    print("Select a copy to move")
                    if self._state.player.type == "heuristic":
                        for piece in self._state.player.copies_in_era(self._state.player.focus):
                            enumerated_moves = self._game.enumerate_possible_moves(piece, piece.symbol,
                                                                                piece.row,
                                                                                piece.column,
                                                                                piece.location,
                                                                                self._state.player,
                                                                                self._state.other)
                            move_triple = []
                            move_values = []
                            for move in enumerated_moves[0]:
                                move_triple.append((move[0], move[1], 0, 1))
                                move_values.append(enumerated_moves[1])

                            print(enumerated_moves[0])
                            print(enumerated_moves[1])
                            sys.exit(0)
                            break
                        # self._state.player._calculate_values(self._state.other)
                    break
                    sys.exit(0)
                    copy = self._state.player.get_piece()
                    
                    piece = self._state.player.owns_piece(copy)
                    enumerated_moves = []
                    #if piece cannot move, pick another (earlier check guarantees there is at least one piece that can move at least once)

                    if self._state.other.owns_piece(copy) != None:
                        print("That is not your copy")
                    elif not piece:
                        print("Not a valid copy")
                    elif piece.location != self._state.player.focus:
                        print("Cannot select a copy from an inactive era")
                    else:
                        enumerated_moves_list = self._game.enumerate_possible_moves(piece.symbol,
                                                                                piece.row,
                                                                                piece.column,
                                                                                piece.location,
                                                                                self._state.player,
                                                                                self._state.other)      
                        enumerated_moves = enumerated_moves_list[0]                   
                        if len(enumerated_moves) == 0:
                            print("That copy cannot move")
                        #if chosen piece can only move once, then check if there is at least one pieec that can move twice
                        elif len(enumerated_moves) == 1:
                            if all_player_pieces == 2:
                                print("Select a copy that can move more than once")  
                        else:                      
                            break
                directions = ['n', 'e', 's', 'w', 'f', 'b']
                print(enumerated_moves)
                while True:
                    print("Select the first direction to move ", directions)
                    move1 = self._state.player.get_move1(enumerated_moves)
                    #ADDED: checks to see if the chosen move is within possible moves
                    if not move1 in directions or all(x[0] != move1 for x in enumerated_moves):
                        print(f"Cannot move {move1}")
                    else:
                        break
                while True:
                    #essentially, if the first move chosen results in no second move being able to be made
                    if not any(x[0] == move1 and x[1] != None for x in enumerated_moves):
                        move2 = None
                        break
                    
                    print("Select the second direction to move ", directions)
                    move2 = self._state.player.get_move2(move1, enumerated_moves)
                    #checks to see if there is one viable move with move1 and move2. If so, move2 is valid
                    if not move2 in directions or not any(x[0] == move1 and x[1] == move2 for x in enumerated_moves):
                        print(f"Cannot move {move2}")
                    else:
                        break
            while True:
                eras = ['past', 'present', 'future']
                print("Select the next era to focus on ['past', 'present', 'future']")
                focus_era = self._state.player.get_focus(self._state.player.focus)
                # if focus_era not in eras or abs(eras.index(focus_era) - self._state.player.focus) > 1:
                #CHANGE: slight bug in original, if in past, couldn't move to future
                if focus_era not in eras or focus_era == self._state.player.focus:
                    print("Not a valid era")
                elif eras.index(focus_era) == self._state.player.focus:
                    print("Cannot select the current era")
                else:
                    break
            print(f"Selected move: {copy},{move1},{move2},{focus_era}")
            if copy == None:
                piece = None
            self._state.run_turn(piece, move1, move2, eras.index(focus_era))

            self._turns += 1
        again = input("Play again?\n")
        if again == "yes":
            print("restart game")
        else:
            sys.exit(0)

class Player1State():
    def __init__(self, cli, player):
        self._cli = cli
        self.player = player
        self.other = cli.player2

    def run_turn(self, piece, move1, move2, era_index):
        if piece != None:
            self.player.move_piece(piece, move1, piece.row, piece.column, self._cli._game)
            self.player.move_piece(piece, move2, piece.row, piece.column, self._cli._game)
        self.player.focus = era_index
        self._cli.set_state(Player2State(self._cli, self._cli.player2))

class Player2State():
    def __init__(self, cli, player):
        self._cli = cli
        self.player = player
        self.other = cli.player1

    def run_turn(self, piece, move1, move2, era_index):
        if piece != None:
            self.player.move_piece(piece, move1, piece.row, piece.column, self._cli._game)
            self.player.move_piece(piece, move2, piece.row, piece.column, self._cli._game)
        self.player.focus = era_index
        self._cli.set_state(Player1State(self._cli, self._cli.player1))
        
class SaveStates():
    def __init__(self):
        self._history =  []

    def run_turn(self, piece, move1, move2, era_index):
        if piece != None:
            self.player.move_piece(piece, move1, piece.row, piece.column, self._cli._game)
            self.player.move_piece(piece, move2, piece.row, piece.column, self._cli._game)
        self.player.focus = era_index
        self._cli.set_state(Player1State(self._cli, self._cli.player1))

if __name__ == "__main__":
    player1 = "human"
    player2 = "human"
    history = "off"
    display = "off"
    for index, arg in enumerate(sys.argv[1:], start=1): #What is these vals are invalid?
        if index == 1:
            player1 = sys.argv[index]
        if index == 2:
            player2 = sys.argv[index]
        if index == 3:
            history = sys.argv[index]
        if index == 4:
            display = sys.argv[index]
    CLI(player1, player2, history, display).run()
    