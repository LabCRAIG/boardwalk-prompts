from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from copy import deepcopy

# Define player enums
class Player:
    PLAYER_1 = 0
    PLAYER_2 = 1

# Game subclass definition
class Amethyst(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = Player.PLAYER_1
        self.capture_chain = False  # Flag to track if a player is in a capture chain

    def prompt_current_player(self):
        return input(f"Player {self.current_player + 1}'s move: ")

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        if is_placement(move):
            return False  # No placements allowed in Amethyst

        if is_movement(move):
            (origin, destination) = get_move_elements(move)
            origin_row, origin_col = origin
            dest_row, dest_col = destination

            # Check if origin is within bounds and contains a valid piece for the current player
            if not (0 <= origin_row < 8 and 0 <= origin_col < 8):
                return False
            piece = self.board.layout[origin_row, origin_col]
            if self.current_player == Player.PLAYER_1 and piece not in ['A', 'Â']:
                return False
            if self.current_player == Player.PLAYER_2 and piece not in ['O', 'Ô']:
                return False

            # Check if destination is within bounds and blank
            if not (0 <= dest_row < 8 and 0 <= dest_col < 8):
                return False
            if self.board.layout[dest_row, dest_col] != '_':
                return False

            # Check if the move is diagonal
            row_diff = abs(dest_row - origin_row)
            col_diff = abs(dest_col - origin_col)
            if row_diff != col_diff:
                return False

            # Check if the move is valid based on piece type
            if piece in ['A', 'O']:
                if (piece == 'A' and dest_row >= origin_row) or (piece == 'O' and dest_row <= origin_row):
                    return False  # A's can only move up, O's can only move down
            if row_diff == 1:
                return True  # Simple diagonal move
            elif row_diff == 2:
                # Check if it's a capture move
                mid_row = (origin_row + dest_row) // 2
                mid_col = (origin_col + dest_col) // 2
                mid_piece = self.board.layout[mid_row, mid_col]
                if self.current_player == Player.PLAYER_1 and mid_piece in ['O', 'Ô']:
                    return True
                if self.current_player == Player.PLAYER_2 and mid_piece in ['A', 'Â']:
                    return True
            return False

        return False

    def perform_move(self, move):
        (origin, destination) = get_move_elements(move)
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        piece = self.board.layout[origin_row, origin_col]

        # Handle capture
        row_diff = abs(dest_row - origin_row)
        if row_diff == 2:
            mid_row = (origin_row + dest_row) // 2
            mid_col = (origin_col + dest_col) // 2
            self.board.layout[mid_row, mid_col] = '_'  # Remove captured piece
            self.capture_chain = True  # Enable capture chain
        else:
            self.capture_chain = False

        # Move the piece
        self.board.move_piece(move)

        # Promote pieces if they reach the end row
        if dest_row == 0 and piece == 'A':
            self.board.layout[dest_row, dest_col] = 'Â'
        if dest_row == 7 and piece == 'O':
            self.board.layout[dest_row, dest_col] = 'Ô'

    def game_finished(self):
        # Check if either player has no pieces left
        player_1_pieces = np.isin(self.board.layout, ['A', 'Â']).sum()
        player_2_pieces = np.isin(self.board.layout, ['O', 'Ô']).sum()
        if player_1_pieces == 0 or player_2_pieces == 0:
            return True

        # Check if the current player has any valid moves
        for row in range(8):
            for col in range(8):
                piece = self.board.layout[row, col]
                if (self.current_player == Player.PLAYER_1 and piece in ['A', 'Â']) or \
                   (self.current_player == Player.PLAYER_2 and piece in ['O', 'Ô']):
                    # Check all possible moves for this piece
                    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < 8 and 0 <= new_col < 8:
                            if self.board.layout[new_row, new_col] == '_':
                                return False
                        if 0 <= new_row + dr < 8 and 0 <= new_col + dc < 8:
                            if self.board.layout[new_row + dr, new_col + dc] == '_':
                                mid_piece = self.board.layout[new_row, new_col]
                                if (self.current_player == Player.PLAYER_1 and mid_piece in ['O', 'Ô']) or \
                                   (self.current_player == Player.PLAYER_2 and mid_piece in ['A', 'Â']):
                                    return False
        return True

    def get_winner(self):
        player_1_pieces = np.isin(self.board.layout, ['A', 'Â']).sum()
        player_2_pieces = np.isin(self.board.layout, ['O', 'Ô']).sum()
        if player_1_pieces == 0 or not self.has_valid_moves(Player.PLAYER_1):
            return Player.PLAYER_2
        if player_2_pieces == 0 or not self.has_valid_moves(Player.PLAYER_2):
            return Player.PLAYER_1
        return None

    def next_player(self):
        if self.capture_chain:
            return self.current_player  # Continue capturing
        return Player.PLAYER_2 if self.current_player == Player.PLAYER_1 else Player.PLAYER_1

    def has_valid_moves(self, player):
        for row in range(8):
            for col in range(8):
                piece = self.board.layout[row, col]
                if (player == Player.PLAYER_1 and piece in ['A', 'Â']) or \
                   (player == Player.PLAYER_2 and piece in ['O', 'Ô']):
                    # Check all possible moves for this piece
                    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < 8 and 0 <= new_col < 8:
                            if self.board.layout[new_row, new_col] == '_':
                                return True
                        if 0 <= new_row + dr < 8 and 0 <= new_col + dc < 8:
                            if self.board.layout[new_row + dr, new_col + dc] == '_':
                                mid_piece = self.board.layout[new_row, new_col]
                                if (player == Player.PLAYER_1 and mid_piece in ['O', 'Ô']) or \
                                   (player == Player.PLAYER_2 and mid_piece in ['A', 'Â']):
                                    return True
        return False

    def finish_message(self, winner):
        if winner is not None:
            print(f"Player {winner + 1} wins!")
        else:
            print("The game is a draw!")

# Initial board setup
initial_layout = (
    " O O O O\n"
    "O O O O \n"
    " O O O O\n"
    "_ _ _ _ \n"
    " _ _ _ _\n"
    "A A A A \n"
    " A A A A\n"
    "A A A A "
)

if __name__ == '__main__':
    board = Board((8, 8), initial_layout)
    mygame = Amethyst(board)
    mygame.game_loop()