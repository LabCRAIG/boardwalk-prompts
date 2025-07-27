from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class Violet(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts
        self.round = 1

    def initial_player(self):
        return 1

    def validate_move(self, move: str) -> bool:
        # Validate whether a move is legal
        if is_movement(move):
            start, end = get_move_elements(move)
            piece = "A" if self.current_player == 1 else "V"

            # Check if the starting position holds the current player's piece
            if self.board.layout[start] != piece:
                return False

            # Check if the destination is empty
            if self.board.layout[end] != "_":
                return False

            # Ensure the move is in a straight line (orthogonal/diagonal)
            dx = np.sign(end[0] - start[0])
            dy = np.sign(end[1] - start[1])
            if dx != 0 and dy != 0 and abs(dx) != abs(dy):
                return False

            # Ensure all spaces between start and end are free
            x, y = start
            while (x, y) != end:
                x, y = x + dx, y + dy
                if (x, y) != end and self.board.layout[x, y] != "_":
                    return False

            return True

        elif is_placement(move):
            # Validate shot placement
            piece, target = get_move_elements(move)
            shooter = piece  # The piece that made the move
            if shooter not in ["A", "V"]:
                return False
            if self.board.layout[target] != "_":
                return False

            # Ensure target is in the shooter's line of sight
            dx = np.sign(target[0] - shooter[0])
            dy = np.sign(target[1] - shooter[1])
            if dx != 0 and dy != 0 and abs(dx) != abs(dy):
                return False

            # Ensure all spaces between the shooter and target are free
            x, y = shooter
            while (x, y) != target:
                x, y = x + dx, y + dy
                if (x, y) != target and self.board.layout[x, y] != "_":
                    return False

            return True

        return False

    def perform_move(self, move: str):
        # Perform the player's move (movement or shot)
        if is_movement(move):
            start, end = get_move_elements(move)
            self.board.move_piece(move)

        elif is_placement(move):
            piece, position = get_move_elements(move)
            self.board.place_piece(move)

    def game_finished(self) -> bool:
        # Check if the game is over (either player has no valid moves)
        for player in [1, 2]:
            piece = "A" if player == 1 else "V"
            for x in range(self.board.height):
                for y in range(self.board.width):
                    if self.board.layout[x, y] == piece:
                        # Check if this piece has any valid moves
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                if dx == 0 and dy == 0:
                                    continue
                                nx, ny = x + dx, y + dy
                                while 0 <= nx < 10 and 0 <= ny < 10:
                                    if self.board.layout[nx, ny] != "_":
                                        break
                                    if self.validate_move(f"{x},{y} {nx},{ny}"):
                                        return False
                                    nx, ny = nx + dx, ny + dy
        return True

    def get_winner(self) -> int:
        # Determine the winner (the other player if the current player cannot move)
        if not self.has_valid_moves(self.current_player):
            return 3 - self.current_player

    def next_player(self) -> int:
        # Alternate between players
        return 3 - self.current_player

    def finish_message(self, winner):
        print(f"Player {winner} wins!")


if __name__ == '__main__':
    # Initialize the board with the proper layout
    layout = (
        "___V__V___\n"
        "__________\n"
        "__________\n"
        "V________V\n"
        "__________\n"
        "__________\n"
        "A________A\n"
        "__________\n"
        "__________\n"
        "___A__A___"
    )
    board = Board((10, 10), layout)
    game = Violet(board)
    game.game_loop()