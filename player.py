import string
from piece import Piece


class Player:
    def __init__(self, id):
        self.id = id
        self._all_pieces = []

        if self.id == "white":
            self._focus = 0
            
            #adds 7 pieces to a player's piece list
            for x in range(0, 7):
                new_piece = Piece(x)
                self._all_pieces.append(new_piece)
                
        else:
            self._focus = 2
            
            #adds 7 pieces to a player's piece list
            for x in range(0, 7):
                new_piece = Piece(string.ascii_lowercase[x])
                self._all_pieces.append(new_piece)      

    #TO DO: Implement simplest version of move
    #TO DO LATER: Add viable moves

    #Owns piece method that will be called CLI

    def get_next_piece(self):
        return Piece("A")