import random
import string
from piece import Piece
from movestrategy import Move, PushMove

class Player:
    '''
    Represents a player object, either "black" or "white" id, as well as either "human," "random" ai, or "heuristic" ai
    '''
    def __init__(self, player_id, player_type):
        '''
        Initializes a player object with a series of 7 Piece instances. 
        '''
        self.type = player_type
        self.id = player_id
        self.all_pieces = []

        if self.id == "white":
            self.focus = 0
            
            #Adds 7 pieces to a player's piece list
            for x in range(0, 7):
                new_piece = Piece(string.ascii_uppercase[x])
                self.all_pieces.append(new_piece)     
                
        else:
            self.focus = 2
            
            #Adds 7 pieces to a player's piece list
            for x in range(0, 7):
                new_piece = Piece(str(x+1))
                self.all_pieces.append(new_piece)
             
    def copies_in_era(self, era):
        '''
        Returns all alive and in_play pieces in a certain era of a Player.
        '''
        return [piece for piece in self.all_pieces if piece.in_play == True and piece.location == era]

    def owns_piece(self, symbol):
        '''
        Returns the Piece object corresponging to a symbol. Else, if there is no match, None is returned.
        '''
        for piece in self.all_pieces:
            if symbol == piece.symbol:
                return piece
        return None        

    def get_next_piece(self):
        '''
        Returns the next piece of in a Player's Piece list that is alive and currently not in play
        '''
        #Returns next valid piece
        for x in self.all_pieces:
            if x.in_play == False and x.alive == True:
                return x
        return None #added this

    def _supply(self):
        supply = []
        for x in self.all_pieces:
            if x.in_play == False and x.alive == True:
                supply.append(x)
        return supply
    
    def _calculate_centrality(self):
        centrality = 0
        for x in self.all_pieces:
            if x.in_play == True and x.alive == True:
                if x.row > 0 and x.row < 3 and x.column > 0 and x.column < 3:
                    centrality += 1
        return centrality
    
    def move_piece(self, piece, direction, row, column, game):
        """
        Moves a piece in accordance to a direction, calling upon Game's own move_piece. 
        """
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
        '''
        Receives human player input for their chosen object.
        '''
        if self.type== "human":
            copy = input()
            return str(copy)

    def get_focus_value(self, era):
        """
        Calculates the focus value of a certain era.
        """
        weight = 2 #this being 1 and the last two elements of criteria weights being set also being 1 also works
        return len(self.copies_in_era(era)) * weight

    def get_unweighted_focus_value(self, era):
        """
        Calculates the number of copies in an era.
        """
        return len(self.copies_in_era(era))

    def calculate_values(self, other):
        """
        Calculates values for a player's score.
        """
        weights = [3,6,2,2] #this doesn't include focus
        criteria = self.get_values(other)
        zipped = zip(weights, criteria)
        value = 0
        for w,c in zipped:
            value += w * c
        return value
    
    def get_values(self, other):
        """
        calculates the necessary information of a player's score.
        """
        era_prescence = 0
        piece_advantage = 0
        for i in range(0,3):
            if self.copies_in_era(i):
                era_prescence += 1
                piece_advantage += len(self.copies_in_era(i))
        for i in range(0,3):
            if other.copies_in_era(i):
                piece_advantage -= len(other.copies_in_era(i))
        supply = len(self._supply())
        centrality = self._calculate_centrality()
        criteria = [era_prescence, piece_advantage, supply, centrality]
        return criteria

    def get_move1(self, enumerated_moves):
        '''
        Receives human player input for their first move.
        '''
        if self.type== "human":
            copy = input()
            return str(copy)         
    
    def get_move2(self, move1, enumerated_moves):
        '''
        Receives human player input for their second move.
        '''
        if self.type== "human":
            copy = input()
            return str(copy)
    
    def get_focus(self, focus):
        '''
        Receives human player input for their new focus.
        '''
        focus = str(focus)
        if self.type== "human":
            copy = input()
            return str(copy) 