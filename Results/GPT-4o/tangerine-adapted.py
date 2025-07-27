from game import Game, Board, is_placement, get_move_elements

class TangerineGame(Game):
    def __init__(self, board):
        # Initialize the base class with the board
        super().__init__(board)
        self.pieces = {0: "H", 1: "V"}  # Player 0 uses 'H', Player 1 uses 'V'

    def initial_player(self):
        """Player 0 (Player 1 in original implementation) starts."""
        return 0

    def validate_move(self, move):
        """Check if the move is valid for the current player."""
        # Ensure the move is a valid placement
        if not is_placement(move):
            return False

        piece, (x, y) = get_move_elements(move)
        if piece != self.pieces[self.current_player]:
            return False  # Ensure the piece corresponds to the current player

        # Validate the placement of the piece on the board
        if piece == "H":  # Horizontal piece
            return (
                0 <= x < self.board.height
                and 0 <= y < self.board.width - 1  # Ensure within bounds
                and self.board.layout[x, y] == "_"  # Ensure the space is blank
                and self.board.layout[x, y + 1] == "_"
            )
        elif piece == "V":  # Vertical piece
            return (
                0 <= x < self.board.height - 1
                and 0 <= y < self.board.width  # Ensure within bounds
                and self.board.layout[x, y] == "_"
                and self.board.layout[x + 1, y] == "_"
            )
        return False

    def perform_move(self, move):
        """Place the piece on the board."""
        piece, (x, y) = get_move_elements(move)
        if piece == "H":
            # Place horizontal piece
            self.board.place_piece(f"{piece} {x},{y}")
            self.board.place_piece(f"{piece} {x},{y + 1}")
        elif piece == "V":
            # Place vertical piece
            self.board.place_piece(f"{piece} {x},{y}")
            self.board.place_piece(f"{piece} {x + 1},{y}")

    def game_finished(self):
        """Check if the game is finished (current player has no valid moves)."""
        piece = self.pieces[self.current_player]
        for x in range(self.board.height):
            for y in range(self.board.width):
                # Check if the current player can place a piece
                if self.validate_move(f"{piece} {x},{y}"):
                    return False
        return True
    
    def next_player(self):
        return self.get_winner()

    def get_winner(self):
        """Return the winner of the game."""
        # The winner is the opponent of the player who cannot make a move
        return 1 - self.current_player

    def finish_message(self, winner):
        """Print the game-over message."""
        print(f"Player {winner + 1} wins!")  # Convert 0/1 back to Player 1/2


if __name__ == "__main__":
    # Initialize a 6x6 board with blank spaces
    board = Board((6, 6))
    game = TangerineGame(board)
    game.game_loop()