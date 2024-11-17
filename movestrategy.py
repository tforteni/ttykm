from abc import ABC, abstractmethod
from board import Board

class MoveStrategy(ABC):
    @abstractmethod
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        pass

class Move(MoveStrategy):
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        print("calling basic move\n")
        if not leave_copy:
            board.remove_piece(piece.row, piece.column)
        board.add_piece(row, column, piece)

class PushMove(MoveStrategy):
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        print("calling push move\n")
        pushed_piece = board.occupied(row, column)
        if not leave_copy:
            board.remove_piece(piece.row, piece.column)
        board.remove_piece(row, column)
        player.move_piece(pushed_piece, direction, pushed_piece.row, pushed_piece.column, game)
        board.add_piece(row, column, piece)
