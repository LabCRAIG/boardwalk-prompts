from game import Game, Board, is_placement, get_move_elements
import numpy as np

# Game subclass definition
class Quartz(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.players = {0: 'A', 1: 'V'}  # Player 1 uses 'A', Player 2 uses 'V'

    def initial_player(self):
        return 0  # Player 1 starts

    def validate_move(self, move: str) -> bool:
        if not is_placement(move):
            return False
        
        piece, (row, col) = get_move_elements(move)

        # Ensure the piece matches the current player
        if piece != self.players[self.current_player]:
            return False

        # Ensure the target space is blank
        if self.board.layout[row, col] != '_':
            return False

        # Check if the move is valid (flips at least one line of opponent's pieces)
        return self.can_flip_pieces(row, col, piece)

    def perform_move(self, move: str):
        piece, (row, col) = get_move_elements(move)
        
        # Place the piece
        self.board.place_piece(move)

        # Flip opponent's pieces in all valid directions
        self.flip_pieces(row, col, piece)

    def game_finished(self) -> bool:
        # The game ends when the board is full or neither player can make a move
        if not np.any(self.board.layout == '_'):
            return True
        return not any(self.can_player_move(player) for player in self.players.keys())

    def get_winner(self) -> int:
        # Count the pieces for each player
        counts = {player: np.count_nonzero(self.board.layout == piece) for player, piece in self.players.items()}
        if counts[0] > counts[1]:
            return 0
        elif counts[1] > counts[0]:
            return 1
        else:
            return None  # Draw

    def next_player(self) -> int:
        return 1 - self.current_player  # Alternate between players

    def can_flip_pieces(self, row: int, col: int, piece: str) -> bool:
        # Check all directions for valid flips
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        opponent_piece = self.players[1 - self.current_player]
        for dx, dy in directions:
            if self.check_line(row, col, dx, dy, piece, opponent_piece):
                return True
        return False

    def check_line(self, row: int, col: int, dx: int, dy: int, piece: str, opponent_piece: str) -> bool:
        # Check if placing a piece here would flip a line of opponent's pieces
        x, y = row + dx, col + dy
        found_opponent = False
        while 0 <= x < self.board.height and 0 <= y < self.board.width:
            if self.board.layout[x, y] == opponent_piece:
                found_opponent = True
            elif self.board.layout[x, y] == piece:
                return found_opponent
            else:
                break
            x, y = x + dx, y + dy
        return False

    def flip_pieces(self, row: int, col: int, piece: str):
        # Flip opponent's pieces in all valid directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        opponent_piece = self.players[1 - self.current_player]
        for dx, dy in directions:
            if self.check_line(row, col, dx, dy, piece, opponent_piece):
                self.flip_line(row, col, dx, dy, piece, opponent_piece)

    def flip_line(self, row: int, col: int, dx: int, dy: int, piece: str, opponent_piece: str):
        # Flip a line of opponent's pieces
        x, y = row + dx, col + dy
        while self.board.layout[x, y] == opponent_piece:
            self.board.layout[x, y] = piece
            x, y = x + dx, y + dy

    def can_player_move(self, player: int) -> bool:
        # Check if the player has any valid moves
        piece = self.players[player]
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == '_' and self.can_flip_pieces(row, col, piece):
                    return True
        return False

if __name__ == '__main__':
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
    board = Board(shape=(8, 8), layout=initial_layout)
    game = Quartz(board)
    game.game_loop()