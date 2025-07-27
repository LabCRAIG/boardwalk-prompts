from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from copy import deepcopy

class Reversi(Game):
    def __init__(self, board):
        super().__init__(board)
        # Initialize the starting positions for Reversi
        self.board.place_piece("W 3,3")
        self.board.place_piece("B 3,4")
        self.board.place_piece("B 4,3")
        self.board.place_piece("W 4,4")
        # Player 0 is Black (B), Player 1 is White (W)
        self.current_player = 0

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            if self.board.layout[row][col] != '_':
                return False  # Cannot place on a non-blank space

            # Check if the move flips at least one opponent piece
            return self._can_flip(piece, row, col)
        return False

    def _can_flip(self, piece, row, col):
        opponent = 'B' if piece == 'W' else 'W'
        directions = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),          (0, 1),
                     (1, -1),  (1, 0), (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board.layout[r][c] == opponent:
                to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board.layout[r][c] == piece and to_flip:
                return True
        return False

    def perform_move(self, move):
        piece, (row, col) = get_move_elements(move)
        self.board.place_piece(move)
        self._flip_pieces(piece, row, col)

    def _flip_pieces(self, piece, row, col):
        opponent = 'B' if piece == 'W' else 'W'
        directions = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),          (0, 1),
                     (1, -1),  (1, 0), (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board.layout[r][c] == opponent:
                to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board.layout[r][c] == piece and to_flip:
                for (fr, fc) in to_flip:
                    self.board.place_piece(f"{piece} {fr},{fc}")

    def game_finished(self):
        # Check if no valid moves are left for either player
        for row in range(8):
            for col in range(8):
                if self.board.layout[row][col] == '_':
                    if self._can_flip('B', row, col) or self._can_flip('W', row, col):
                        return False
        return True

    def get_winner(self):
        black_count = np.count_nonzero(self.board.layout == 'B')
        white_count = np.count_nonzero(self.board.layout == 'W')
        if black_count > white_count:
            return 0  # Black wins
        elif white_count > black_count:
            return 1  # White wins
        else:
            return None  # Draw

    def next_player(self):
        return 1 - self.current_player  # Alternate between 0 (Black) and 1 (White)

    def prompt_current_player(self):
        player = "Black (B)" if self.current_player == 0 else "White (W)"
        return input(f"{player}'s move: ")

    def finish_message(self, winner):
        if winner is None:
            print("The game is a draw!")
        else:
            winner_name = "Black" if winner == 0 else "White"
            print(f"{winner_name} wins!")

if __name__ == '__main__':
    board = Board((8, 8))
    mygame = Reversi(board)
    mygame.game_loop()