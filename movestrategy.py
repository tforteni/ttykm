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
            board.remove_piece(piece.row, piece.column, piece)
        #ADDED: NOT SURE IF YOU WANT THIS, CURRENT SYSTEM DOESN'T CHECK TO SEE IF A PUSHED PIECE IS OUT OF BOUNDS
        if (0 <= row <= board._rows and 0 <= column <= board._columns):
            board.add_piece(row, column, piece, game.all_boards.index(board))
        else:
            board.remove_piece(row, column, piece)


class TimeMove(MoveStrategy):
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        print("calling time travel move\n")
        dirs = {
            "f": 1,
            "b": -1}
        old_board = game.all_boards[game.all_boards.index(board) - dirs[direction]]
        if direction == "b":
            leave_copy = True #if copies are 0 then this isn't allowed
        if not leave_copy:
            old_board.remove_piece(piece.row, piece.column, piece)
        board.add_piece(row, column, piece, game.all_boards.index(board))

class PushMove(MoveStrategy):
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        print("calling push move\n")
        dirs = {
            "n": -1,
            "e": 1,
            "s": 1,
            "w": -1}
        pushed_piece = board.occupied(row, column)
        if not leave_copy:
            board.remove_piece(piece.row, piece.column, piece)
        if direction in ["n", "s"] and (pushed_piece.row + dirs[direction] > 3 or pushed_piece.row + dirs[direction]) < 0 or direction in ["e", "w"] and (pushed_piece.column + dirs[direction] > 3 or pushed_piece.column + dirs[direction]) < 0:
            board.kill_piece(row, column, pushed_piece)
        else:
            board.remove_piece(row, column, piece)
            player.move_piece(pushed_piece, direction, pushed_piece.row, pushed_piece.column, game)
        board.add_piece(row, column, piece, game.all_boards.index(board))
