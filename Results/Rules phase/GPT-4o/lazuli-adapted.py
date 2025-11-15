from game import Game, Board, is_movement, get_move_elements


class Lazuli(Game):
    def __init__(self, board):
        super().__init__(board)
        # No additional state is needed for this game

    def validate_move(self, move):
        """Check if the move is valid according to Lazuli rules."""
        if not is_movement(move):
            return False

        # Extract start and end positions
        (sx, sy), (ex, ey) = get_move_elements(move)

        # Ensure start and end positions are within bounds
        if not (0 <= sx < self.board.height and 0 <= sy < self.board.width
                and 0 <= ex < self.board.height and 0 <= ey < self.board.width):
            return False

        # The start position must have an "X" piece
        if self.board.layout[sx][sy] != "X":
            return False

        # The end position must be blank
        if self.board.layout[ex][ey] != "_":
            return False

        # Determine the position of the piece being jumped over
        mx, my = (sx + ex) // 2, (sy + ey) // 2

        # Check if the move is horizontal or vertical and spans exactly 2 cells
        if abs(sx - ex) == 2 and sy == ey:  # Vertical move
            return self.board.layout[mx][my] == "X"
        elif abs(sy - ey) == 2 and sx == ex:  # Horizontal move
            return self.board.layout[mx][my] == "X"

        # Invalid move otherwise
        return False

    def perform_move(self, move):
        """Execute a valid move, updating the board and removing the jumped piece."""
        if not self.validate_move(move):
            raise ValueError("Invalid move")

        # Extract start and end positions
        (sx, sy), (ex, ey) = get_move_elements(move)

        # Determine the position of the piece being jumped over
        mx, my = (sx + ex) // 2, (sy + ey) // 2

        # Perform the move
        self.board.layout[sx][sy] = "_"  # Clear the starting position
        self.board.layout[mx][my] = "_"  # Remove the jumped piece
        self.board.layout[ex][ey] = "X"  # Place the piece at the destination

    def game_finished(self):
        """Check if the game has ended (win or no moves left)."""
        return self.is_win() or not self.has_moves_left()

    def get_winner(self):
        """Determine the winner of the game."""
        if self.is_win():
            return 1  # Player wins
        return None  # No winner (loss)

    def is_win(self):
        """Check if the player has won."""
        remaining_pieces = sum(row.count("X") for row in self.board.layout)
        return remaining_pieces == 1 and self.board.layout[3][3] == "X"

    def has_moves_left(self):
        """Check if there are any valid moves left."""
        for x in range(self.board.height):
            for y in range(self.board.width):
                if self.board.layout[x][y] == "X":
                    # Check all possible moves from this position
                    possible_moves = [
                        f"{x},{y} {x+2},{y}",  # Down
                        f"{x},{y} {x-2},{y}",  # Up
                        f"{x},{y} {x},{y+2}",  # Right
                        f"{x},{y} {x},{y-2}",  # Left
                    ]
                    if any(self.validate_move(move) for move in possible_moves):
                        return True
        return False

    def finish_message(self, winner):
        """Display a custom endgame message."""
        if winner == 1:
            print("Congratulations! You win!")
        else:
            print("No moves left. You lose!")


if __name__ == "__main__":
    # Define the initial board layout for Lazuli
    initial_layout = (
        "  XX   \n"
        "  XX   \n"
        "XXXXXXX\n"
        "XXX_XXX\n"
        "XXXXXXX\n"
        "  XX   \n"
        "  XX   "
    )

    # Create the board and game instance
    board = Board((7, 7), initial_layout)
    game = Lazuli(board)
    game.game_loop()