from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from copy import deepcopy

# Game subclass definition
class Obsidian(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts
        self.initial_f_moves = {'f': set(), 'F': set()}  # Track initial moves for f and F

    def prompt_current_player(self):
        return input(f"Player {self.current_player}, your move: ")

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        if is_movement(move):
            (origin, destination) = get_move_elements(move)
            piece = self.board.layout[origin]
            if not self._is_valid_piece(piece):
                return False
            return self._is_valid_movement(piece, origin, destination)
        else:
            return False  # Only movements are allowed

    def _is_valid_piece(self, piece):
        if self.current_player == 1:
            return piece in {'a', 'b', 'c', 'd', 'e', 'f'}
        else:
            return piece in {'A', 'B', 'C', 'D', 'E', 'F'}

    def _is_valid_movement(self, piece, origin, destination):
        (x1, y1), (x2, y2) = origin, destination
        dx, dy = x2 - x1, y2 - y1
        target_piece = self.board.layout[destination]

        # Check if destination is occupied by a friendly piece
        if target_piece != '_' and (self.current_player == 1 and target_piece.islower() or self.current_player == 2 and target_piece.isupper()):
            return False

        # Movement rules for each piece
        if piece.lower() == 'f':
            return self._is_valid_f_move(piece, origin, destination)
        elif piece.lower() == 'a':
            return self._is_valid_a_move(origin, destination)
        elif piece.lower() == 'c':
            return self._is_valid_c_move(origin, destination)
        elif piece.lower() == 'b':
            return self._is_valid_b_move(origin, destination)
        elif piece.lower() == 'e':
            return self._is_valid_e_move(origin, destination)
        elif piece.lower() == 'd':
            return self._is_valid_d_move(origin, destination)
        return False

    def _is_valid_f_move(self, piece, origin, destination):
        (x1, y1), (x2, y2) = origin, destination
        dx, dy = x2 - x1, y2 - y1
        target_piece = self.board.layout[destination]

        # Define forward direction
        forward = -1 if piece == 'f' else 1

        # Check if it's the first move
        if piece not in self.initial_f_moves:
            self.initial_f_moves[piece] = set()
        is_first_move = origin not in self.initial_f_moves[piece]

        # Movement logic
        if dx == forward and abs(dy) == 1:  # Diagonal capture
            return target_piece != '_' and (self.current_player == 1 and target_piece.isupper() or self.current_player == 2 and target_piece.islower())
        elif dx == forward and dy == 0:  # Forward move
            return target_piece == '_'
        elif is_first_move and dx == 2 * forward and dy == 0:  # Double forward on first move
            intermediate = (x1 + forward, y1)
            return self.board.layout[intermediate] == '_' and target_piece == '_'
        return False

    def _is_valid_a_move(self, origin, destination):
        (x1, y1), (x2, y2) = origin, destination
        dx, dy = x2 - x1, y2 - y1
        if dx != 0 and dy != 0:
            return False  # Must move orthogonally
        return self._is_path_clear(origin, destination)

    def _is_valid_c_move(self, origin, destination):
        (x1, y1), (x2, y2) = origin, destination
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) != abs(dy):
            return False  # Must move diagonally
        return self._is_path_clear(origin, destination)

    def _is_valid_b_move(self, origin, destination):
        (x1, y1), (x2, y2) = origin, destination
        dx, dy = x2 - x1, y2 - y1
        return (abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2)

    def _is_valid_e_move(self, origin, destination):
        return self._is_path_clear(origin, destination)

    def _is_valid_d_move(self, origin, destination):
        (x1, y1), (x2, y2) = origin, destination
        dx, dy = x2 - x1, y2 - y1
        return abs(dx) <= 1 and abs(dy) <= 1

    def _is_path_clear(self, origin, destination):
        (x1, y1), (x2, y2) = origin, destination
        dx, dy = x2 - x1, y2 - y1
        steps = max(abs(dx), abs(dy))
        x_step, y_step = dx // steps, dy // steps
        for i in range(1, steps):
            if self.board.layout[(x1 + i * x_step, y1 + i * y_step)] != '_':
                return False
        return True

    def perform_move(self, move):
        if is_movement(move):
            (origin, destination) = get_move_elements(move)
            piece = self.board.layout[origin]
            self.board.move_piece(move)

            # Handle promotion of f/F
            if piece.lower() == 'f':
                if (self.current_player == 1 and destination[0] == 0) or (self.current_player == 2 and destination[0] == 7):
                    self.board.place_piece(f"{'e' if piece == 'f' else 'E'} {destination[0]},{destination[1]}")

            # Track initial moves for f/F
            if piece in {'f', 'F'}:
                self.initial_f_moves[piece].add(origin)

    def game_finished(self):
        # Check if D or d has been captured
        return not any('D' in row for row in self.board.layout) or not any('d' in row for row in self.board.layout)

    def get_winner(self):
        if not any('D' in row for row in self.board.layout):
            return 1
        elif not any('d' in row for row in self.board.layout):
            return 2
        return None

    def next_player(self):
        return 2 if self.current_player == 1 else 1

    def finish_message(self, winner):
        if winner is None:
            print("The game is a draw!")
        else:
            print(f"Player {winner} wins!")

# Initial board setup
initial_layout = """\
ABCDECBA
FFFFFFFF
________
________
________
________
ffffffff
abcdecba\
"""

if __name__ == '__main__':
    board = Board((8, 8), initial_layout)
    mygame = Obsidian(board)
    mygame.game_loop()