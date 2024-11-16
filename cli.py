from game import Game

class CLI:
    """Display the CLI menu and respond to choices when run."""

    def __init__(self):
        self._selected_account = None
        self._game = Game()
        self._player1 = Player(white)
        self._player2 = Player(black)
        self.state = Player1State()

    def set_current_player(self, player):
        """Sets the current state(player)."""
        self._current_player = player

    def run(self):
        """Display the game and menu and respond to choices."""
        while True: #Or while the game is not over
            self._game.show_game()
            copy = input("Select a copy to move\n")
            move1 = input("Select the first direction to move ['n', 'e', 's', 'w', 'f', 'b']")
            move2 = input("Select the second direction to move ['n', 'e', 's', 'w', 'f', 'b']")
            focus_era = input("Select the next era to focus on ['past', 'present', 'future']")
            print(f"Selected move: {copy},{move1},{move2},{era})")

class Player1State():

class Player2State():

if __name__ == "__main__":
    CLI().run()