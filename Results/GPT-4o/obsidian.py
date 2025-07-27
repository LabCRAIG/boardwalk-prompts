from game import Game, Board, is_movement, get_move_elements
import numpy as np

class Obsidian(Game):
    def __init__(self, board):
        super().__init__(board)
        self.first_moves = {}  # Tracks whether a piece has moved yet (for F/f two-step rule)
        for i in range(8):
            self.first_moves[(1, i)] = True  # Player 2's F pieces
            self.first_moves[(6, i)] = True  # Player 1's f pieces

    def initial_player(self):
        return 0  # Player 1 starts

    def next_player(self):
        return 1 - self.current_player  # Alternate between players 0 and 1

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        if is_movement(move):
            start, end = get_move_elements(move)
            piece = self.board.layout[start]

            # Verify movement is valid for the given piece
            if piece.islower() and self.current_player != 0:
                return False  # Player 1 controls lowercase pieces
            if piece.isupper() and self.current_player != 1:
                return False  # Player 2 controls uppercase pieces
            return self._validate_piece_move(piece, start, end)
        return False  # Placement is not allowed in Obsidian

    def _validate_piece_move(self, piece, start, end):
        r1, c1 = start
        r2, c2 = end
        dr, dc = r2 - r1, c2 - c1
        dest_piece = self.board.layout[end]

        # General rules: destination must be free or occupied by an opponent
        if dest_piece != "_" and dest_piece.islower() == piece.islower():
            return False

        # Movement rules for each piece
        if piece.lower() == "f":
            direction = 1 if piece.isupper() else -1  # Forward direction
            if dr == direction and abs(dc) == 1 and dest_piece != "_":  # Diagonal capture
                return True
            if dr == direction and dc == 0 and dest_piece == "_":  # One-step forward
                return True
            if self.first_moves.get((r1, c1), False) and dr == 2 * direction and dc == 0:
                # Two-step forward for unmoved F/f
                mid_r = r1 + direction
                if self.board.layout[mid_r, c1] == "_" and dest_piece == "_":
                    return True
            return False
        elif piece.lower() == "a":
            return self._validate_linear_move(start, end, orthogonal=True)
        elif piece.lower() == "c":
            return self._validate_linear_move(start, end, orthogonal=False)
        elif piece.lower() == "b":
            return abs(dr) == 2 and abs(dc) == 1 or abs(dr) == 1 and abs(dc) == 2
        elif piece.lower() == "e":
            return self._validate_linear_move(start, end, orthogonal=True) or self._validate_linear_move(start, end, orthogonal=False)
        elif piece.lower() == "d":
            return abs(dr) <= 1 and abs(dc) <= 1
        return False

    def _validate_linear_move(self, start, end, orthogonal):
        r1, c1 = start
        r2, c2 = end
        dr, dc = r2 - r1, c2 - c1

        # Check if move is orthogonal (row or column only) or diagonal (row == column move)
        if orthogonal and not (dr == 0 or dc == 0):
            return False
        if not orthogonal and abs(dr) != abs(dc):
            return False

        # Ensure all spaces between start and end are free
        steps = max(abs(dr), abs(dc))
        step_r = dr // steps if dr != 0 else 0
        step_c = dc // steps if dc != 0 else 0
        for i in range(1, steps):
            if self.board.layout[r1 + i * step_r, c1 + i * step_c] != "_":
                return False
        return True

    def perform_move(self, move):
        super().perform_move(move)
        if is_movement(move):
            start, end = get_move_elements(move)
            piece = self.board.layout[end]
            # Handle f/F promotion
            if piece == "f" and end[0] == 0:
                self.board.layout[end] = "e"
            elif piece == "F" and end[0] == 7:
                self.board.layout[end] = "E"
            # Mark piece as having moved
            if (start in self.first_moves):
                self.first_moves[start] = False

    def game_finished(self):
        # Game ends when one player's D or d is captured
        layout = self.board.layout
        return "D" not in layout or "d" not in layout

    def get_winner(self):
        # Player 1 wins if D is captured, Player 2 wins if d is captured
        layout = self.board.layout
        if "D" not in layout:
            return 0
        elif "d" not in layout:
            return 1
        return None  # Draw is not possible in Obsidian

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("It's a draw!")

if __name__ == "__main__":
    initial_layout = (
        "ABCDECBA\n"
        "FFFFFFFF\n"
        "________\n"
        "________\n"
        "________\n"
        "________\n"
        "ffffffff\n"
        "abcdecba"
    )
    board = Board((8, 8), initial_layout)
    game = Obsidian(board)
    game.game_loop()