from game import Game, Board, is_movement, get_move_elements
import numpy as np

class Lazuli(Game):
    def __init__(self, board):
        super().__init__(board)
        self.piece = 'X'  # The only piece type in the game

    def validate_move(self, move):
        # Ensure the move is a valid movement
        if not is_movement(move):
            return False

        # Extract move elements
        (origin, destination) = get_move_elements(move)
        (x1, y1), (x2, y2) = origin, destination

        # Check if origin and destination are within bounds
        if not (0 <= x1 < self.board.height and 0 <= y1 < self.board.width and
                0 <= x2 < self.board.height and 0 <= y2 < self.board.width):
            return False

        # Check if the origin has a piece and the destination is blank
        if self.board.layout[x1][y1] != self.piece or self.board.layout[x2][y2] != '_':
            return False

        # Check if the move is a valid jump (horizontal or vertical)
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) == 2 and dy == 0:  # Vertical jump
            jumped_x, jumped_y = x1 + dx // 2, y1
        elif abs(dy) == 2 and dx == 0:  # Horizontal jump
            jumped_x, jumped_y = x1, y1 + dy // 2
        else:
            return False

        # Check if the jumped space has a piece
        if self.board.layout[jumped_x][jumped_y] != self.piece:
            return False

        return True

    def perform_move(self, move):
        # Extract move elements
        (origin, destination) = get_move_elements(move)
        (x1, y1), (x2, y2) = origin, destination

        # Move the piece
        self.board.layout[x2][y2] = self.piece
        self.board.layout[x1][y1] = '_'

        # Remove the jumped piece
        jumped_x, jumped_y = (x1 + x2) // 2, (y1 + y2) // 2
        self.board.layout[jumped_x][jumped_y] = '_'

    def game_finished(self):
        # Check if only one piece remains and it is in the center
        piece_count = np.count_nonzero(self.board.layout == self.piece)
        center_x, center_y = self.board.height // 2, self.board.width // 2
        if piece_count == 1 and self.board.layout[center_x][center_y] == self.piece:
            return True

        # Check if no valid moves are left
        for x in range(self.board.height):
            for y in range(self.board.width):
                if self.board.layout[x][y] == self.piece:
                    # Check all possible jumps
                    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        x2, y2 = x + dx, y + dy
                        if 0 <= x2 < self.board.height and 0 <= y2 < self.board.width:
                            move = f"{x},{y} {x2},{y2}"
                            if self.validate_move(move):
                                return False
        return True

    def get_winner(self):
        # If only one piece remains and it is in the center, the player wins
        piece_count = np.count_nonzero(self.board.layout == self.piece)
        center_x, center_y = self.board.height // 2, self.board.width // 2
        if piece_count == 1 and self.board.layout[center_x][center_y] == self.piece:
            return 0  # Player wins
        return None  # Player loses

    def finish_message(self, winner):
        if winner == 0:
            print("Congratulations! You won!")
        else:
            print("Game over. You lost.")

# Initial board setup
initial_layout = (
    "  XXXXX\n"
    "  XXXXX\n"
    "XXXXXXX\n"
    "XXXX_XX\n"
    "XXXXXXX\n"
    "  XXXXX\n"
    "  XXXXX"
)

if __name__ == '__main__':
    board = Board((7, 7), initial_layout)
    mygame = Lazuli(board)
    mygame.game_loop()