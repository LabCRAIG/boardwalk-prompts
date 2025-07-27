from game import Game, Board, is_movement, is_placement, get_move_elements
from copy import deepcopy
import numpy as np

# Game subclass definition
class Quartz(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts
        self.player_pieces = {1: 'A', 2: 'V'}  # Player 1 uses 'A', Player 2 uses 'V'

    def validate_move(self, move):
        # Check if the move is valid according to the game rules
        if not super().validate_move(move):
            return False

        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            if piece != self.player_pieces[self.current_player]:
                return False  # Players can only place their own pieces

            # Check if the placement is adjacent to an opponent's piece
            adjacent_opponent = False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < self.board.height and 0 <= c < self.board.width:
                        if self.board.layout[r][c] == self.player_pieces[3 - self.current_player]:
                            adjacent_opponent = True
                            break
                if adjacent_opponent:
                    break

            if not adjacent_opponent:
                return False

            # Check if the placement sandwiches opponent pieces
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < self.board.height and 0 <= c < self.board.width:
                        if self.board.layout[r][c] == self.player_pieces[3 - self.current_player]:
                            # Check if there's a player's piece in the same line
                            r2, c2 = r + dr, c + dc
                            while 0 <= r2 < self.board.height and 0 <= c2 < self.board.width:
                                if self.board.layout[r2][c2] == self.player_pieces[self.current_player]:
                                    return True
                                if self.board.layout[r2][c2] == '_':
                                    break
                                r2 += dr
                                c2 += dc
            return False

        return False  # Only placements are allowed in Quartz

    def perform_move(self, move):
        # Perform the move and flip sandwiched pieces
        piece, (row, col) = get_move_elements(move)
        self.board.place_piece(move)

        # Flip sandwiched pieces in all directions
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                to_flip = []
                while 0 <= r < self.board.height and 0 <= c < self.board.width:
                    if self.board.layout[r][c] == self.player_pieces[3 - self.current_player]:
                        to_flip.append((r, c))
                    elif self.board.layout[r][c] == self.player_pieces[self.current_player]:
                        for flip_r, flip_c in to_flip:
                            self.board.place_piece(f"{self.player_pieces[self.current_player]} {flip_r},{flip_c}")
                        break
                    else:
                        break
                    r += dr
                    c += dc

    def game_finished(self):
        # Check if the board is full or no valid moves remain
        if np.count_nonzero(self.board.layout == '_') == 0:
            return True

        # Check if both players have no valid moves
        for player in [1, 2]:
            self.current_player = player
            for row in range(self.board.height):
                for col in range(self.board.width):
                    if self.board.layout[row][col] == '_':
                        move = f"{self.player_pieces[player]} {row},{col}"
                        if self.validate_move(move):
                            self.current_player = 1  # Reset current player
                            return False
        self.current_player = 1  # Reset current player
        return True

    def get_winner(self):
        # Count pieces for each player
        count_A = np.count_nonzero(self.board.layout == 'A')
        count_V = np.count_nonzero(self.board.layout == 'V')
        if count_A > count_V:
            return 1
        elif count_V > count_A:
            return 2
        else:
            return None  # Draw

    def next_player(self):
        # Alternate between players
        return 3 - self.current_player

    def finish_message(self, winner):
        if winner is None:
            print("The game is a draw!")
        else:
            print(f"Player {winner} wins!")

# Initial board setup
initial_layout = (
    "________\n"
    "________\n"
    "________\n"
    "___AV___\n"
    "___VA___\n"
    "________\n"
    "________\n"
    "________"
)

if __name__ == '__main__':
    board = Board((8, 8), initial_layout)
    mygame = Quartz(board)
    mygame.game_loop()