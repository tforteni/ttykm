import random
import string
from piece import Piece
from movestrategy import Move, PushMove

class Player:
    def __init__(self, id, type):
        self.type = type
        self.id = id
        self._all_pieces = []

        if self.id == "white":
            self.focus = 0
            
            #Adds 7 pieces to a player's piece list
            for x in range(0, 7):
                new_piece = Piece(string.ascii_uppercase[x])
                self._all_pieces.append(new_piece)     
                
        else:
            self.focus = 2
            
            #Adds 7 pieces to a player's piece list
            for x in range(0, 7):
                new_piece = Piece(str(x+1))
                self._all_pieces.append(new_piece)
             

    #TO DO: Implement simplest version of move
    #TO DO LATER: Add viable moves

    def copies_in_era(self, era):
        return [piece for piece in self._all_pieces if piece.in_play == True and piece.location == era]

    def owns_piece(self, symbol):
        for piece in self._all_pieces:
            if symbol == piece.symbol:
                return piece
        return None

    def get_next_piece(self):
        #Returns next valid piece
        for x in self._all_pieces:
            if x.in_play == False and x.alive == True:
                return x
    
    def move_piece(self, piece, direction, row, column, game):
        print("calling player move piece\n")
        dirs = {
            "n": -1,
            "e": 1,
            "s": 1,
            "w": -1,
            "f": 1,
            "b": -1}
        board = piece.location
        if direction in ["e", "w"]:
            row += dirs[direction]
        if direction in ["n", "s"]:
            column += dirs[direction]
        if direction in ["f", "b"]:
            board += dirs[direction]
        game.move_piece(piece, row, column, board, game, self, direction)
    
    def get_piece(self):
        if self.type== "human":
            copy = input()
            return str(copy)
        elif self.type== "random":
            matching_pieces = [x for x in self._all_pieces if x.location == self.focus and x.alive == True and x.in_play == True]
            copy = str(random.choice(matching_pieces))
            print(copy)
            return copy
    
    def get_move1(self, enumerated_moves):
        if self.type== "human":
            copy = input()
            return str(copy)
        elif self.type== "random":
            self.all_move = random.choice(enumerated_moves)
            move1 = str(self.all_move[0])
            print(move1)
            return move1
    
    def get_move2(self, move1, enumerated_moves):
        if self.type== "human":
            copy = input()
            return str(copy)
        elif self.type== "random":
            move2 = str(self.all_move[1])
            print(move2)
            return move2
    
    def get_focus(self, focus):
        focus = str(focus)
        if self.type== "human":
            copy = input()
            return str(copy)
        elif self.type== "random":
            dict = {"0": "past", "1": "present", "2": "future"}
            list = ["past", "present", "future"]
            list.remove(dict[focus])
            
            copy = random.choice(list)
            print(copy)
            return copy

if __name__ == "__main__":
    walter = Player("white", "human")
    