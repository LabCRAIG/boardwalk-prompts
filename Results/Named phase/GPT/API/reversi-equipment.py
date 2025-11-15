
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
import numpy as np

class Reversi(Game):
    class Player(Enum):
        BLACK = 0
        WHITE = 1

    def __init__(self, board):
        super().__init__(board)
        self.current_player = self.Player.BLACK.value

    def validate_move(self, move: str) -> bool:
        if not super().validate_move(move):
            return False

        if not is_placement(move):
            return False

        piece, (x, y) = get_move_elements(move)

        # Ensure the piece is valid for the current player
        if (self.current_player == self.Player.BLACK.value and piece != 'B') or \
           (self.current_player == self.Player.WHITE.value and piece != 'W'):
            return False

        # Ensure the move is within bounds
        if not (0 <= x < self.board.height and 0 <= y < self.board.width):
            return False

        # Ensure the space is blank
        if self.board.layout[x, y] != '_':
            return False

        # Prevent placement in the 2x2 corner zones
        corners = [(0, 0), (0, 1), (1, 0), (1, 1),  # Top-left corner
                   (0, self.board.width - 2), (0, self.board.width - 1),
                   (1, self.board.width - 2), (1, self.board.width - 1),  # Top-right corner
                   (self.board.height - 2, 0), (self.board.height - 1, 0),
                   (self.board.height - 2, 1), (self.board.height - 1, 1),  # Bottom-left corner
                   (self.board.height - 2, self.board.width - 2), (self.board.height - 1, self.board.width - 2),
                   (self.board.height - 2, self.board.width - 1), (self.board.height - 1, self.board.width - 1)]  # Bottom-right corner
        if (x, y) in corners:
            return False

        # Ensure the move flips at least one piece
        return self._can_flip_pieces(x, y)

    def _can_flip_pieces(self, x, y) -> bool:
        opponent_piece = 'W' if self.current_player == self.Player.BLACK.value else 'B'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            has_opponent = False

            while 0 <= nx < self.board.height and 0 <= ny < self.board.width:
                if self.board.layout[nx, ny] == opponent_piece:
                    has_opponent = True
                elif self.board.layout[nx, ny] == ('B' if self.current_player == self.Player.BLACK.value else 'W'):
                    if has_opponent:
                        return True
                    break
                else:
                    break

                nx += dx
                ny += dy

        return False

    def perform_move(self, move: str):
        super().perform_move(move)
        piece, (x, y) = get_move_elements(move)

        # Flip opponent pieces
        self._flip_pieces(x, y, piece)

    def _flip_pieces(self, x, y, piece):
        opponent_piece = 'W' if piece == 'B' else 'B'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            to_flip = []
            nx, ny = x + dx, y + dy

            while 0 <= nx < self.board.height and 0 <= ny < self.board.width:
                if self.board.layout[nx, ny] == opponent_piece:
                    to_flip.append((nx, ny))
                elif self.board.layout[nx, ny] == piece:
                    for fx, fy in to_flip:
                        self.board.layout[fx, fy] = piece
                    break
                else:
                    break

                nx += dx
                ny += dy

    def game_finished(self) -> bool:
        # Check if either player can make a move
        for x in range(self.board.height):
            for y in range(self.board.width):
                if self.board.layout[x, y] == '_':
                    if self._can_flip_pieces(x, y):
                        return False

        return True

    def get_winner(self) -> int:
        black_count = np.count_nonzero(self.board.layout == 'B')
        white_count = np.count_nonzero(self.board.layout == 'W')

        if black_count > white_count:
            return self.Player.BLACK.value
        elif white_count > black_count:
            return self.Player.WHITE.value
        else:
            return None

    def next_player(self) -> int:
        return (self.current_player + 1) % 2


if __name__ == '__main__':
    initial_layout = (
        "        \n"
        "        \n"
        "        \n"
        "   WB   \n"
        "   BW   \n"
        "        \n"
        "        \n"
        "        "
    )
    board = Board((8, 8), initial_layout)
    reversi = Reversi(board)
    reversi.game_loop()
