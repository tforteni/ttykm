from abc import ABC, abstractmethod
from board import Board

class MoveStrategy(ABC):
    @abstractmethod
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        pass

class Move(MoveStrategy):
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        # print("calling basic move")
        if not leave_copy:
            board.remove_piece(piece.row, piece.column, piece)
        board.add_piece(row, column, piece, game.all_boards.index(board))

class TimeMove(MoveStrategy):
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        # print("calling time travel move")
        dirs = {
            "f": 1,
            "b": -1}
        old_board = game.all_boards[game.all_boards.index(board) - dirs[direction]]
        if direction == "b":
            leave_copy = True #if copies are 0 then this isn't allowed
        old_info = [piece.row, piece.column]
        next_piece = player.get_next_piece()
        old_board.remove_piece(piece.row, piece.column, piece)
        if leave_copy == True:
            old_board.add_piece(old_info[0], old_info[1], next_piece, game.all_boards.index(old_board))
        board.add_piece(row, column, piece, game.all_boards.index(board))

class PushMove(MoveStrategy):
    def move(self, game, piece, row, column, board, player, direction, leave_copy):
        str(direction)
        # print("calling push move")
        dirs = {
            "n": -1,
            "e": 1,
            "s": 1,
            "w": -1,
            "None" : 0}
        pushed_piece = board.occupied(row, column)
        if direction == None:
            return
        if not leave_copy:
            board.remove_piece(piece.row, piece.column, piece)
        if ((direction in ["e", "w"] and (pushed_piece.row + dirs[direction] > 3) or pushed_piece.row + dirs[direction] < 0)) or (direction in ["s", "n"] and (pushed_piece.column + dirs[direction] > 3 or pushed_piece.column + dirs[direction] < 0)):
            board.kill_piece(row, column, pushed_piece)
        else:
            board.remove_piece(row, column, piece)
            player.move_piece(pushed_piece, direction, pushed_piece.row, pushed_piece.column, game)
        board.add_piece(row, column, piece, game.all_boards.index(board))
