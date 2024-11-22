from abc import ABC, abstractmethod
from board import Board

class MoveStrategy(ABC):
    '''
    An abstract class to aid in the creation of more specific move strategies.
    '''
    @abstractmethod
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        pass

class Move(MoveStrategy):
    """
    A MoveStrategy that moves a piece based on a non-time and non-push move. 
    """
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        '''
        Moves a piece to a new location. 
        '''
        if not leave_copy:
            board.remove_piece(piece.row, piece.column, piece)
        board.add_piece(row, column, piece, game.all_boards.index(board))

class TimeMove(MoveStrategy):
    '''
    A MoveStrategy that moves a piece based on wheter or not that Piece moved through time.
    '''
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        '''
        Moves a piece to a new location, as well as determining whether or not a copy must be placed.
        '''
        dirs = {
            "f": 1,
            "b": -1}
        old_board = game.all_boards[game.all_boards.index(board) - dirs[direction]]
        if direction == "b":
            leave_copy = True
        old_info = [piece.row, piece.column]
        next_piece = player.get_next_piece()
        old_board.remove_piece(piece.row, piece.column, piece)
        if leave_copy == True:
            old_board.add_piece(old_info[0], old_info[1], next_piece, game.all_boards.index(old_board))
        board.add_piece(row, column, piece, game.all_boards.index(board))

class PushMove(MoveStrategy):
    """
    A MoveStrategy that moves a piece based on a push move.
    """
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        '''
        Moves a piece to a new location, as well as determining whether or not a push has resulted in the death
        of a piece through a push out of the board or a push that caused a paradox.
        '''
        dirs = {
            "n": -1,
            "e": 1,
            "s": 1,
            "w": -1,
            "None" : 0}
        pushed_piece = board.occupied(row, column)
        paradox = False
        if direction == None:
            return
        if not leave_copy:
            board.remove_piece(piece.row, piece.column, piece)
        if ((direction in ["e", "w"] and (pushed_piece.row + dirs[direction] > 3) or pushed_piece.row + dirs[direction] < 0)) or (direction in ["s", "n"] and (pushed_piece.column + dirs[direction] > 3 or pushed_piece.column + dirs[direction] < 0)):
            if player.owns_piece(piece.symbol) and player.owns_piece(pushed_piece.symbol):
                paradox = True
                board.kill_piece(row, column, piece)
                board.kill_piece(pushed_piece.row, pushed_piece.column, pushed_piece)
            else:
                board.kill_piece(row, column, pushed_piece)
        else:
            if player.owns_piece(piece.symbol) and player.owns_piece(pushed_piece.symbol):
                paradox = True
                board.kill_piece(row, column, piece)
                board.kill_piece(pushed_piece.row, pushed_piece.column, pushed_piece)
            else:
                board.remove_piece(row, column, piece)
                player.move_piece(pushed_piece, direction, pushed_piece.row, pushed_piece.column, game)
        if not paradox:
            board.add_piece(row, column, piece, game.all_boards.index(board))
