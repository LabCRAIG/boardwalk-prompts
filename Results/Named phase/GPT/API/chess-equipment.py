
from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

# Enum to represent players
class Player:
    WHITE = 0
    BLACK = 1

# Chess Game class
class Chess(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.initial_knight_positions()

    def initial_knight_positions(self):
        """Place knights at the center four spaces as per the modified rule."""
        center_positions = [(3, 3), (3, 4), (4, 3), (4, 4)]
        knights = ['N', 'n', 'N', 'n']  # White knights ('N') and black knights ('n')
        for position, knight in zip(center_positions, knights):
            move = f"{knight} {position[0]},{position[1]}"
            self.board.place_piece(move)

    def validate_move(self, move: str) -> bool:
        """Validate the player's move."""
        if not super().validate_move(move):
            return False

        if is_placement(move):
            return False  # No placements allowed after initial board setup

        if is_movement(move):
            origin, destination = get_move_elements(move)
            piece = self.board.layout[origin]
            target = self.board.layout[destination]

            # Ensure the piece belongs to the current player
            if piece.isupper() and self.current_player != Player.WHITE:
                return False
            if piece.islower() and self.current_player != Player.BLACK:
                return False

            # Ensure players move their knights according to knight's movement rules
            dx = abs(origin[0] - destination[0])
            dy = abs(origin[1] - destination[1])
            if (dx, dy) not in [(2, 1), (1, 2)]:  # Valid knight moves
                return False

            # Ensure the destination is either empty or contains an opponent's piece
            if target != '_' and (piece.isupper() == target.isupper()):
                return False

            return True

        return False

    def perform_move(self, move: str):
        """Perform the player's move."""
        if is_movement(move):
            origin, destination = get_move_elements(move)
            piece = self.board.layout[origin]

            # Move the piece and replace the origin with a blank space
            self.board.move_piece(move)

    def game_finished(self) -> bool:
        """Check if the game has finished."""
        # Game ends when either player has no knights left
        flattened_board = self.board.layout.flatten()
        white_knights = any(piece == 'N' for piece in flattened_board)
        black_knights = any(piece == 'n' for piece in flattened_board)
        return not (white_knights and black_knights)

    def get_winner(self) -> int:
        """Determine the winner."""
        flattened_board = self.board.layout.flatten()
        white_knights = any(piece == 'N' for piece in flattened_board)
        black_knights = any(piece == 'n' for piece in flattened_board)

        if white_knights and not black_knights:
            return Player.WHITE
        if black_knights and not white_knights:
            return Player.BLACK
        return None  # Draw

    def next_player(self) -> int:
        """Determine the next player."""
        return Player.BLACK if self.current_player == Player.WHITE else Player.WHITE

    def finish_message(self, winner):
        """Print the end of game message."""
        if winner is None:
            print("The game is a draw!")
        else:
            print(f"Player {winner} wins!")

if __name__ == '__main__':
    # Initialize the board for a standard 8x8 Chess game
    layout = (
        "rnbqkbnr"
        "pppppppp"
        "________"
        "________"
        "________"
        "________"
        "PPPPPPPP"
        "RNBQ_BNR"  # Knights are removed from their usual starting positions
    )
    board = Board((8, 8), layout)
    mygame = Chess(board)
    mygame.game_loop()
