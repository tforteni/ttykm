from game import Game
from player import Player

class CLI:
    """Display the CLI menu and respond to choices when run."""

    def __init__(self):
        self._selected_account = None
        self._game = Game()
        self.player1 = Player("white")
        self.player2 = Player("black")
        self._state = Player1State(self, self.player1)

    def set_state(self, new_state):
        """Sets the current state(player)."""
        self._state = new_state

    def run(self):
        """Display the game and menu and respond to choices."""
        while True: #Or while the game is not over
            self._game.show_game()
            copy = input("Select a copy to move\n")
            move1 = input("Select the first direction to move ['n', 'e', 's', 'w', 'f', 'b']\n")
            move2 = input("Select the second direction to move ['n', 'e', 's', 'w', 'f', 'b']\n")
            focus_era = input("Select the next era to focus on ['past', 'present', 'future']\n")
            print(f"Selected move: {copy},{move1},{move2},{focus_era}")
            self._state.run_turn()

class Player1State():
    def __init__(self, cli, player):
        self._cli = cli
        self._player = player

    def run_turn(self):
        print("white just played")
        self._cli.set_state(Player2State(self._cli, self._cli.player2))

class Player2State():
    def __init__(self, cli, player):
        self._cli = cli
        self._player = player

    def run_turn(self):
        print("black just played")
        self._cli.set_state(Player1State(self._cli, self._cli.player1))

if __name__ == "__main__":
    CLI().run()