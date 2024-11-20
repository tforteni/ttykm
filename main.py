from abc import ABC, abstractmethod
import copy
import sys
import random
from game import Game
from player import Player

class CLI:
    """Display the CLI menu and respond to choices when run."""

    def __init__(self, player1, player2, history, display):
        self.player1 = Player("white", player1)
        self.player2 = Player("black", player2)
        self._game = Game(self.player1, self.player2)
        self._turns = 1
        self._state = Player1State(self, self.player1)
        self._history = history
        self._display = display
        self._caretaker = Caretaker(self)


    def set_state(self, new_state):
        """Sets the current state(player)."""
        self._state = new_state
    
    def _print_scores(self):
        if self._state.player == self.player1:
            white_score = self._state.player.get_values(self._state.other)
            white_focus = self._state.player.get_unweighted_focus_value(self._state.player.focus)
            black_score = self._state.other.get_values(self._state.player)
            black_focus = self._state.other.get_unweighted_focus_value(self._state.other.focus)
        else:
            black_score = self._state.player.get_values(self._state.other)
            white_score = self._state.other.get_values(self._state.player)
            black_focus = self._state.player.get_unweighted_focus_value(self._state.player.focus)
            white_focus = self._state.other.get_unweighted_focus_value(self._state.other.focus)
        print(f"white's score: {white_score[0]} eras, {white_score[1]} advantage, {white_score[2]} supply, {white_score[3]} centrality, {white_focus} in focus")
        print(f"black's score: {black_score[0]} eras, {black_score[1]} advantage, {black_score[2]} supply, {black_score[3]} centrality, {black_focus} in focus")

    def run(self):
        """Display the game and menu and respond to choices."""
        self._game.build_game()
        while not self._game.is_over(self._state.player, self._state.other): #Or while the game is not over
            # self._caretaker.backup()
            self._game.show_game()
            #TO DO: Advanced error checking
            print(f"Turn: {self._turns}, Current player: {self._state.player.id}")
            if self._display == "on":
                self._print_scores()
                # if self._state.player == self.player1:
                #     white_score = self._state.player.get_values(self._state.other)
                #     white_focus = self._state.player.get_unweighted_focus_value(self._state.player.focus)
                #     black_score = self._state.other.get_values(self._state.player)
                #     black_focus = self._state.other.get_unweighted_focus_value(self._state.other.focus)
                # else:
                #     black_score = self._state.player.get_values(self._state.other)
                #     white_score = self._state.other.get_values(self._state.player)
                #     black_focus = self._state.player.get_unweighted_focus_value(self._state.player.focus)
                #     white_focus = self._state.other.get_unweighted_focus_value(self._state.other.focus)
                # print(f"white's score: {white_score[0]} eras, {white_score[1]} advantage, {white_score[2]} supply, {white_score[3]} centrality, {white_focus} in focus")
                # print(f"black's score: {black_score[0]} eras, {black_score[1]} advantage, {black_score[2]} supply, {black_score[3]} centrality, {black_focus} in focus")
            
            if self._history == "on":
                self._caretaker.backup()
                print("undo, redo, or next")
                copy = input()
                while copy != "next":
                    if copy == "undo":
                        self._caretaker.undo()
                        # self._game.show_game()
                        # print(f"Turn: {self._turns}, Current player: {self._state.player.id}")
                    elif copy == "redo":
                        self._caretaker.redo()
                        # self._game.show_game()
                        # print(f"Turn: {self._turns}, Current player: {self._state.player.id}")
                    self._game.show_game()
                    print(f"Turn: {self._turns}, Current player: {self._state.player.id}")
                    self._print_scores()
                    print("undo, redo, or next")
                    copy = input()
                self._caretaker.remove_branches()
    
            #Gives a number from 0, 1, and 2. The max number of moves all pieces are able to move.
            #0- all pieces cannot move at all
            #1- at least one piece can move once
            #2- at least one piece can move twice

            all_player_pieces = self._game.better_pieces(self._state.player) #This doesn't seem to work for heuristics

            eras = ['past', 'present', 'future']
            if self._state.player.type == "random":
                matching_pieces = [x for x in self._state.player.all_pieces if x.location == self._state.player.focus and x.alive == True and x.in_play == True]
                if len(matching_pieces) == 0:
                    piece = None
                    copy = None
                    move1 = None
                    move2 = None
                else:
                    piece = random.choice(matching_pieces)
                    copy = piece.symbol
                
                    enumerated_moves = self._game.enumerate_possible_moves(piece, piece.symbol,
                                                        piece.row,
                                                        piece.column,
                                                        piece.location,
                                                        self._state.player,
                                                        self._state.other)
                    if len(enumerated_moves) == 0 or len(enumerated_moves[0]) == 0:
                        move1 = None
                        move2 = None
                    else:
                        self.all_move = random.choice(enumerated_moves[0])
                        move1 = str(self.all_move[0])
                        move2 = str(self.all_move[1])
                
                eras_dict = {0: "past", 1: "present", 2: "future"}
                eras_list = ["past", "present", "future"]
                eras_list.remove(eras_dict[self._state.player.focus])
                
                focus_era = random.choice(eras_list)

            elif self._state.player.type == "heuristic":
                heuristic_moves = {}
                if (self._state.player.focus == 0):
                    era1 = 1
                    era2 = None
                elif (self._state.player.focus == 1):
                    era1 = 0
                    era2 = 2
                elif (self._state.player.focus == 2):
                    era1 = 1
                    era2 = None
                for piece in self._state.player.copies_in_era(self._state.player.focus):
                    enumerated_moves = self._game.enumerate_possible_moves(piece, piece.symbol,
                                                                        piece.row,
                                                                        piece.column,
                                                                        piece.location,
                                                                        self._state.player,
                                                                        self._state.other)
                    # print(enumerated_moves[0])
                    if enumerated_moves:
                        for index, move in enumerate(enumerated_moves[0]):
                            new_val = self._state.player.get_focus_value(era1) + enumerated_moves[1][index]
                            heuristic_moves[(piece, move[0], move[1], era1)] = new_val
                            if era2:
                                # print(enumerated_moves[1][index])
                                new_val = self._state.player.get_focus_value(era2) + enumerated_moves[1][index]
                                heuristic_moves[(piece, move[0], move[1], era2)] = new_val

                # print(f"{piece.symbol}, {piece.row}, {piece.column}")
                # print(enumerated_moves[0])
                # print(enumerated_moves[1])
                # print(heuristic_moves.values())

                if len(heuristic_moves) == 0:
                    copy = None
                    move1 = None
                    move2 = None
                    if era1 and era2:
                        era = random.choice([era1, era2])
                    elif not era1:
                        era = era2
                    else:
                        era = era1
                    focus_era = eras[era]
                    # if self._state.player.get_focus_value(era1) > self._state.player.get_focus_value(era2):
                    #     focus_era = eras[era1]
                else: 
                    # print(heuristic_moves)
                    max_value = max(heuristic_moves.values())
                    # options = {key for key, value in heuristic_moves.items() if value == max_value}
                    options = {key: value for key, value in heuristic_moves.items() if value == max_value}
                    # print(options)
                    move = random.choice(list(options))
                    # print(move)
                    copy = move[0]
                    piece = self._state.player.owns_piece(str(copy))
                    move1 = move[1]
                    move2 = move[2]
                    focus_era = eras[move[3]]
            elif not self._state.player.copies_in_era(self._state.player.focus) or all_player_pieces == 0:
                print("No copies to move")
                copy = None
                move1 = None
                move2 = None
            else:
                while True:
                    print("Select a copy to move")
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
                        enumerated_moves_list = self._game.enumerate_possible_moves(piece, piece.symbol,
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
                while True:
                    print("Select the first direction to move", directions)
                    move1 = self._state.player.get_move1(enumerated_moves)
                    #ADDED: checks to see if the chosen move is within possible moves
                    if not move1 in directions:
                        print("Not a valid direction")
                    elif all(x[0] != move1 for x in enumerated_moves):
                        print(f"Cannot move {move1}")
                    else:
                        break
                while True:
                    #essentially, if the first move chosen results in no second move being able to be made
                    if not any(x[0] == move1 and x[1] != None for x in enumerated_moves):
                        move2 = None
                        break
                    
                    print("Select the second direction to move", directions)
                    move2 = self._state.player.get_move2(move1, enumerated_moves)
                    #checks to see if there is one viable move with move1 and move2. If so, move2 is valid
                    if not move2 in directions or not any(x[0] == move1 and x[1] == move2 for x in enumerated_moves):
                        print(f"Cannot move {move2}")
                    else:
                        break
            if self._state.player.type != "heuristic" and self._state.player.type != "random":
                while True:
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
            # print(copy)
            self._state.run_turn(piece, move1, move2, eras.index(focus_era))
            self._turns += 1
            
        again = input("Play again?\n")
        if again == "yes":
            CLI(player1, player2, history, display).run()
        else:
            sys.exit(0)

    def save(self):
        """
        Saves the current state inside a memento.
        """
        return ConcreteMemento(copy.deepcopy(self._game), 
                               copy.deepcopy(self._turns),
                               copy.deepcopy(self._state),
                               copy.deepcopy(self._history),    
                               copy.deepcopy(self._display))

    def restore(self, memento):
        """
        Restores the Originator's state from a memento object.
        """
        self._game = copy.deepcopy(memento.get_info()[0])

        self.player1 = self._game.player1
        self.player2 = self._game.player2
        self._turns = copy.deepcopy(memento.get_info()[1])

        if isinstance(memento.get_info()[2], Player1State):
            self._state = Player1State(self, self.player1)
        else:
            self._state = Player2State(self, self.player2)
        
        self._game.all_boards = self._game.fill_empty_board()
      
        self._history = copy.deepcopy(memento.get_info()[3])

        self._display = copy.deepcopy(memento.get_info()[4])
        
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
        
class Memento(ABC):
    """
    The Memento interface provides a way to retrieve the memento's metadata,
    such as creation date or name. However, it doesn't expose the Originator's
    state.
    """
    @abstractmethod
    def get_info(self) -> str:
        pass

class ConcreteMemento(Memento):
    def __init__(self, game, turns, state, history, display):
        self._info = [game, turns, state, history, display]

    def get_info(self):
        """
        The Originator uses this method when restoring its state.
        """
        return self._info

class Caretaker():
    """
    The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
    doesn't have access to the originator's state, stored inside the memento. It
    works with all mementos via the base Memento interface.
    """

    def __init__(self, cli) -> None:
        self._mementos = []
        self._cli = cli
        self._index = -1

    def backup(self) -> None:
        # print("\nCaretaker: Saving Originator's state...")
        self._mementos.append(self._cli.save())
        self._index += 1

    def undo(self) -> None:
        # print("stage A")
        if not len(self._mementos):
            return
        # print("stage A2")
        if self._index - 1 < 0:
            return
        # print("stage B")
        memento = self._mementos[self._index - 1]
        self._index += -1
        try:
            self._cli.restore(memento)
        except Exception:
            self.undo()
    
    def redo(self) -> None:
        if not len(self._mementos):
            return
        if self._index + 1 == len(self._mementos):
            return

        memento = self._mementos[self._index + 1]
        self._index += 1

        try:
            self._cli.restore(memento)
        except Exception:
            self.redo()
            
    def remove_branches(self) -> None:
        if not len(self._mementos):
            return       
        while self._mementos[self._index] != self._mementos[-1]:
            self._mementos.pop()                   

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
    # counter = 0
    # while True:
    CLI(player1, player2, history, display).run()
        # counter += 1
        # with open("output.txt", "w") as file:
        #     print(counter, file=file)
    