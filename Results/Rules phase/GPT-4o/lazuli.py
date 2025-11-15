from game import Game, Board, is_movement, get_move_elements
import numpy as np


class Lazuli(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.pieces_left = np.count_nonzero(self.board.layout == 'X')  # Count initial pieces

    def validate_move(self, move: str) -> bool:
        # Ensure the move is properly formatted and is a movement
        if not is_movement(move):
            return False

        # Extract move elements
        origin, destination = get_move_elements(move)
        ox, oy = origin
        dx, dy = destination

        # Verify that the origin and destination are within bounds
        if not (0 <= ox < self.board.height and 0 <= oy < self.board.width):
            return False
        if not (0 <= dx < self.board.height and 0 <= dy < self.board.width):
            return False

        # Verify the origin contains a piece and the destination is blank
        if self.board.layout[ox, oy] != 'X' or self.board.layout[dx, dy] != '_':
            return False

        # Verify the move is horizontal or vertical (no diagonal moves)
        if abs(ox - dx) + abs(oy - dy) != 2:  # Distance must be exactly 2 spaces
            return False

        # Verify there is a piece to jump over
        mx, my = (ox + dx) // 2, (oy + dy) // 2  # Midpoint (piece being jumped over)
        if self.board.layout[mx, my] != 'X':
            return False

        return True

    def perform_move(self, move: str):
        # Extract move elements
        origin, destination = get_move_elements(move)
        ox, oy = origin
        dx, dy = destination
        mx, my = (ox + dx) // 2, (oy + dy) // 2  # Midpoint (piece being jumped over)

        # Perform the move: move piece, remove jumped piece, and update the board
        self.board.move_piece(move)
        self.board.place_piece(f"_ {mx},{my}")  # Remove the jumped piece by setting it to blank
        self.pieces_left -= 1  # Decrease the number of pieces left

    def game_finished(self) -> bool:
        # Game ends if only one piece is left or no valid moves are possible
        if self.pieces_left == 1:
            return True

        # Check for any valid moves
        for x in range(self.board.height):
            for y in range(self.board.width):
                if self.board.layout[x, y] == 'X':  # Found a piece, check its moves
                    for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:  # Possible directions
                        move = f"{x},{y} {x+dx},{y+dy}"
                        if self.validate_move(move):
                            return False  # A valid move exists, game is not finished
        return True

    def get_winner(self) -> int:
        # Check if the last piece is in the center and is the only piece left
        center = (self.board.height // 2, self.board.width // 2)
        if self.pieces_left == 1 and self.board.layout[center] == 'X':
            return 0  # Player wins
        return None  # Player loses

    def finish_message(self, winner):
        if winner is not None:
            print("Congratulations! You won!")
        else:
            print("Game over. No valid moves left. You lose.")

    def next_player(self) -> int:
        return 0  # Only one player, so it always remains the same

    def prompt_current_player(self) -> str:
        # Display the current player and prompt for input
        return input(f"Round {self.round}, make your move (format: 'x1,y1 x2,y2'): ")


if __name__ == '__main__':
    # Define the initial board layout for Lazuli
    initial_layout = (
        "  XX  \n"
        "  XX  \n"
        "XX__XX\n"
        "XX_X_XX\n"
        "XX__XX\n"
        "  XX  \n"
        "  XX  "
    )

    # Create the board and the game
    board = Board((7, 7), initial_layout)
    lazuli_game = Lazuli(board)
    lazuli_game.game_loop()