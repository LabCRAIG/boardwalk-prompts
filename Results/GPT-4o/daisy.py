from game import Game, Board, is_movement, is_placement, get_move_elements
from copy import deepcopy

class Daisy(Game):
    # Player enums for clarity
    PLAYER_1 = 0
    PLAYER_2 = 1

    def __init__(self, board: Board):
        super().__init__(board)
        self.reserve = {
            self.PLAYER_1: {"A": 1, "B": 1, "C": 1, "D": 2, "E": 2, "F": 2, "G": 2, "H": 9},
            self.PLAYER_2: {"a": 1, "b": 1, "c": 1, "d": 2, "e": 2, "f": 2, "g": 2, "h": 9}
        }
        self.a_on_board = {self.PLAYER_1: False, self.PLAYER_2: False}  # Tracks if A/a is on the board

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False

        if is_placement(move):
            piece, position = get_move_elements(move)
            # Check if the piece belongs to the current player and is in reserve
            if piece not in self.reserve[self.current_player] or self.reserve[self.current_player][piece] <= 0:
                return False
            # Check if the target position is a blank space
            x, y = position
            if self.board.layout[x, y] != "_":
                return False
            return True

        elif is_movement(move):
            origin, destination = get_move_elements(move)
            ox, oy = origin
            dx, dy = destination
            piece = self.board.layout[ox, oy]
            target = self.board.layout[dx, dy]

            # Check if the piece at origin belongs to the current player
            if piece not in self.reserve[self.current_player]:
                return False

            # Check if the movement is valid for the specific piece
            if not self.is_valid_piece_move(piece, origin, destination):
                return False

            # Check if the destination is free or contains an opposing piece
            if target == "_" or self.is_opponent_piece(piece, target):
                # Ensure capture is allowed only if A/a is on the board
                if target != "_" and not self.a_on_board[self.current_player]:
                    return False
                return True
        return False

    def is_valid_piece_move(self, piece: str, origin: tuple, destination: tuple) -> bool:
        ox, oy = origin
        dx, dy = destination
        dx_diff, dy_diff = dx - ox, dy - oy

        if piece in "Aa":  # Moves one space in any direction
            return abs(dx_diff) <= 1 and abs(dy_diff) <= 1

        elif piece in "Bb":  # Moves any number of spaces orthogonally
            return (dx_diff == 0 or dy_diff == 0) and self.is_path_clear(origin, destination)

        elif piece in "Cc":  # Moves any number of spaces diagonally
            return abs(dx_diff) == abs(dy_diff) and self.is_path_clear(origin, destination)

        elif piece in "Dd":  # Moves one step in any direction except diagonally backward
            if piece == "D" and dx_diff == -1 and abs(dy_diff) == 1:  # Backward diagonal for uppercase
                return False
            if piece == "d" and dx_diff == 1 and abs(dy_diff) == 1:  # Backward diagonal for lowercase
                return False
            return abs(dx_diff) <= 1 and abs(dy_diff) <= 1

        elif piece in "Ee":  # Moves one square diagonally or one square forward orthogonally
            if abs(dx_diff) == 1 and abs(dy_diff) == 1:
                return True
            if dy_diff == 0 and ((piece == "E" and dx_diff == -1) or (piece == "e" and dx_diff == 1)):
                return True
            return False

        elif piece in "Ff":  # Moves two spaces forward and one to the side
            if (piece == "F" and dx_diff == -2) or (piece == "f" and dx_diff == 2):
                return abs(dy_diff) == 1
            return False

        elif piece in "Gg":  # Moves any number of spaces orthogonally forward
            if dy_diff == 0 and ((piece == "G" and dx_diff < 0) or (piece == "g" and dx_diff > 0)):
                return self.is_path_clear(origin, destination)
            return False

        elif piece in "Hh":  # Moves one space forward orthogonally
            return dy_diff == 0 and ((piece == "H" and dx_diff == -1) or (piece == "h" and dx_diff == 1))

        return False

    def is_path_clear(self, origin: tuple, destination: tuple) -> bool:
        """Check if the path from origin to destination is clear."""
        ox, oy = origin
        dx, dy = destination
        dx_step = 0 if ox == dx else (1 if dx > ox else -1)
        dy_step = 0 if oy == dy else (1 if dy > oy else -1)

        x, y = ox + dx_step, oy + dy_step
        while (x, y) != (dx, dy):
            if self.board.layout[x, y] != "_":
                return False
            x += dx_step
            y += dy_step
        return True

    def is_opponent_piece(self, piece: str, target: str) -> bool:
        """Check if a target piece belongs to the opponent."""
        return (piece.isupper() and target.islower()) or (piece.islower() and target.isupper())

    def perform_move(self, move: str):
        if is_placement(move):
            piece, position = get_move_elements(move)
            x, y = position
            self.board.place_piece(move)
            self.reserve[self.current_player][piece] -= 1
            if piece in "Aa":
                self.a_on_board[self.current_player] = True

        elif is_movement(move):
            origin, destination = get_move_elements(move)
            ox, oy = origin
            dx, dy = destination
            piece = self.board.layout[ox, oy]
            target = self.board.layout[dx, dy]

            if self.is_opponent_piece(piece, target):
                # Capture logic: Add captured piece to reserve
                equivalent_piece = target.upper() if self.current_player == self.PLAYER_1 else target.lower()
                self.reserve[self.current_player][equivalent_piece] += 1

            self.board.move_piece(move)

    def game_finished(self) -> bool:
        return False
        return not any("A" in row for row in self.board.layout) or not any("a" in row for row in self.board.layout)

    def get_winner(self) -> int:
        if not any("A" in row for row in self.board.layout):
            return self.PLAYER_2
        if not any("a" in row for row in self.board.layout):
            return self.PLAYER_1
        return None

    def next_player(self) -> int:
        return self.PLAYER_1 if self.current_player == self.PLAYER_2 else self.PLAYER_2

if __name__ == '__main__':
    board = Board((9, 9))
    daisy_game = Daisy(board)
    daisy_game.game_loop()