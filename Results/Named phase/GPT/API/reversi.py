
from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class Reversi(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.players = {0: 'B', 1: 'W'}  # Black (B) and White (W) players
        self.current_player = self.initial_player()

    def initial_player(self) -> int:
        return 0  # Black plays first

    def validate_move(self, move: str) -> bool:
        if not is_placement(move):
            return False
        
        piece, (x, y) = get_move_elements(move)
        if piece != self.players[self.current_player]:  # Ensure correct piece
            return False
        if not (0 <= x < self.board.height and 0 <= y < self.board.width):  # Check bounds
            return False
        if self.board.layout[x, y] != '_':  # Ensure the space is blank
            return False
        
        # Check at least one direction flips opponent pieces
        return any(self._flips_pieces(x, y, dx, dy) for dx, dy in self._directions())

    def perform_move(self, move: str):
        piece, (x, y) = get_move_elements(move)
        self.board.place_piece(move)  # Place the player's piece
        # Flip opponent pieces in all valid directions
        for dx, dy in self._directions():
            if self._flips_pieces(x, y, dx, dy):
                self._flip_pieces(x, y, dx, dy)

    def game_finished(self) -> bool:
        # Check if either player has valid moves left
        for player in self.players.values():
            if self._has_valid_moves(player):
                return False
        return True

    def get_winner(self) -> int:
        black_count = np.sum(self.board.layout == 'B')
        white_count = np.sum(self.board.layout == 'W')
        if black_count > white_count:
            return 0
        elif white_count > black_count:
            return 1
        return None  # Draw

    def next_player(self) -> int:
        return (self.current_player + 1) % 2

    def _has_valid_moves(self, player_piece: str) -> bool:
        for x in range(self.board.height):
            for y in range(self.board.width):
                if self.board.layout[x, y] == '_' and any(
                    self._flips_pieces(x, y, dx, dy, player_piece)
                    for dx, dy in self._directions()
                ):
                    return True
        return False

    def _flips_pieces(self, x: int, y: int, dx: int, dy: int, player_piece=None) -> bool:
        if player_piece is None:
            player_piece = self.players[self.current_player]
        opponent_piece = self.players[(self.current_player + 1) % 2]

        nx, ny = x + dx, y + dy
        has_opponent_pieces = False
        while 0 <= nx < self.board.height and 0 <= ny < self.board.width:
            if self.board.layout[nx, ny] == opponent_piece:
                has_opponent_pieces = True
            elif self.board.layout[nx, ny] == player_piece:
                return has_opponent_pieces
            else:
                break
            nx, ny = nx + dx, ny + dy
        return False

    def _flip_pieces(self, x: int, y: int, dx: int, dy: int):
        opponent_piece = self.players[(self.current_player + 1) % 2]
        player_piece = self.players[self.current_player]

        nx, ny = x + dx, y + dy
        while 0 <= nx < self.board.height and 0 <= ny < self.board.width:
            if self.board.layout[nx, ny] == opponent_piece:
                self.board.layout[nx, ny] = player_piece
            elif self.board.layout[nx, ny] == player_piece:
                break
            nx, ny = nx + dx, ny + dy

    @staticmethod
    def _directions():
        # All 8 possible directions
        return [(-1, -1), (-1, 0), (-1, 1),
                (0, -1),         (0, 1),
                (1, -1), (1, 0), (1, 1)]

if __name__ == '__main__':
    initial_layout = (
        "________\n"
        "________\n"
        "________\n"
        "___BW___\n"
        "___WB___\n"
        "________\n"
        "________\n"
        "________"
    )
    board = Board((8, 8), initial_layout)
    reversi = Reversi(board)
    reversi.game_loop()
