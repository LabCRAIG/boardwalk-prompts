class Tangerine:
    def __init__(self):
        self.board = [[" " for _ in range(6)] for _ in range(6)]  # 6x6 empty board
        self.current_player = 1  # Player 1 starts
        self.pieces = {1: "H", 2: "V"}  # Player 1 uses 'H', Player 2 uses 'V'

    def display_board(self):
        """Print the current state of the board."""
        print("  " + " ".join(str(i) for i in range(6)))
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))
        print()

    def is_valid_move(self, piece, x, y):
        """Check if placing a piece at (x, y) is valid."""
        if piece == "H":
            # Horizontal piece requires (x, y) and (x, y+1) to be free
            return (
                0 <= x < 6
                and 0 <= y < 5  # Ensure it doesn't go out of bounds horizontally
                and self.board[x][y] == " "
                and self.board[x][y + 1] == " "
            )
        elif piece == "V":
            # Vertical piece requires (x, y) and (x-1, y) to be free
            return (
                0 <= x < 5
                and 0 <= y < 6  # Ensure it doesn't go out of bounds vertically
                and self.board[x][y] == " "
                and self.board[x + 1][y] == " "
            )
        return False

    def place_piece(self, piece, x, y):
        """Place the piece on the board."""
        if piece == "H":
            self.board[x][y] = "H"
            self.board[x][y + 1] = "H"
        elif piece == "V":
            self.board[x][y] = "V"
            self.board[x + 1][y] = "V"

    def has_valid_moves(self):
        """Check if the current player has any valid moves."""
        piece = self.pieces[self.current_player]
        for x in range(6):
            for y in range(6):
                if self.is_valid_move(piece, x, y):
                    return True
        return False

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 1 if self.current_player == 2 else 2

    def play(self):
        """Main game loop."""
        print("Welcome to Tangerine!")
        self.display_board()

        while True:
            print(f"Player {self.current_player}'s turn ({self.pieces[self.current_player]}):")

            # Check if the current player can make a move
            if not self.has_valid_moves():
                print(f"Player {self.current_player} has no valid moves!")
                self.switch_player()
                print(f"Player {self.current_player} wins!")
                break

            # Get input from the player
            try:
                x, y = map(
                    int,
                    input("Enter the coordinates to place your piece (row col): ").split(),
                )
                piece = self.pieces[self.current_player]
                if self.is_valid_move(piece, x, y):
                    self.place_piece(piece, x, y)
                    self.display_board()
                    self.switch_player()
                else:
                    print("Invalid move. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter row and column as integers separated by a space.")

# Run the game
if __name__ == "__main__":
    game = Tangerine()
    game.play()