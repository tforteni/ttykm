from game import Game
from player import Player

class CLI:
    """Display the CLI menu and respond to choices when run."""

    def __init__(self):
        self._selected_account = None
        self.player1 = Player("white")
        self.player2 = Player("black")
        self._game = Game(self.player1, self.player2)
        self._turns = 1
        self._state = Player1State(self, self.player1)

    def set_state(self, new_state):
        """Sets the current state(player)."""
        self._state = new_state

    def run(self):
        """Display the game and menu and respond to choices."""
        self._game.build_game()
        while True: #Or while the game is not over
            self._game.show_game()
            #TO DO: Error checking
            print(f"Turn: {self._turns}, Current player: {self._state.player.id}")
            while True:
                copy = input("Select a copy to move\n")
                copy = str(copy)
                piece = self._state.player.owns_piece(copy)
                if self._state.other.owns_piece(copy):
                    print("That is not your copy")
                elif not piece:
                    print("Not a valid copy")
                elif piece.location != self._state.player.focus:
                    print("Cannot select a copy from an inactive era")
                else:
                    break
            directions = ['n', 'e', 's', 'w', 'f', 'b']
            while True:
                move1 = input(f"Select the first direction to move {directions}\n")
                if not move1 in directions:
                    print(f"Cannot move {move1}")
                else:
                    break
            while True:
                move2 = input(f"Select the second direction to move {directions}\n")
                if not move2 in directions:
                    print(f"Cannot move {move2}")
                else:
                    break
            while True:
                eras = ['past', 'present', 'future']
                focus_era = input("Select the next era to focus on ['past', 'present', 'future']\n")
                if focus_era not in eras:
                    print("Not a valid era")
                elif eras.index(focus_era) == self._state.player.focus:
                    print("Cannot select the current era")
                else:
                    break
            print(f"Selected move: {copy},{move1},{move2},{focus_era}")
            self._state.run_turn()
            self._turns += 1

class Player1State():
    def __init__(self, cli, player):
        self._cli = cli
        self.player = player
        self.other = cli.player2

    def run_turn(self):
        print("white just played")
        self._cli.set_state(Player2State(self._cli, self._cli.player2))

class Player2State():
    def __init__(self, cli, player):
        self._cli = cli
        self.player = player
        self.other = cli.player1

    def run_turn(self):
        print("black just played")
        self._cli.set_state(Player1State(self._cli, self._cli.player1))

if __name__ == "__main__":
    CLI().run()