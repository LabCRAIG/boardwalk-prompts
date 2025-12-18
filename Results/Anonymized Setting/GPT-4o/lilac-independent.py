class LilacGame:
    def __init__(self):
        # Initialize the 7x7 board with the starting setup
        self.board = [
            ["_", "_", "V", "V", "V", "_", "_"],
            ["_", "_", "_", "V", "_", "_", "_"],
            ["V", "_", "A", "A", "A", "_", "V"],
            ["V", "V", "A", "Â", "A", "V", "V"],
            ["V", "_", "A", "A", "A", "_", "V"],
            ["_", "_", "_", "V", "_", "_", "_"],
            ["_", "_", "V", "V", "V", "_", "_"]
        ]
        self.current_player = 1  # Player 1 starts
        self.game_over = False

    def display_board(self):
        # Display the current state of the board
        for row in self.board:
            print(" ".join(row))
        print()

    def is_valid_move(self, x1, y1, x2, y2):
        # Check if the move is valid
        if not (0 <= x1 < 7 and 0 <= y1 < 7 and 0 <= x2 < 7 and 0 <= y2 < 7):
            return False  # Out of bounds
        if self.board[x1][y1] == "_" or self.board[x2][y2] != "_":
            return False  # No piece to move or target not empty
        if abs(x2 - x1) + abs(y2 - y1) != 1:
            return False  # Not an orthogonal move
        piece = self.board[x1][y1]
        if self.current_player == 1 and piece != "V":
            return False  # Player 1 can only move V
        if self.current_player == 2 and piece not in ["A", "Â"]:
            return False  # Player 2 can only move A or Â
        if piece == "Â" and (x2, y2) != (3, 3) and self.board[x2][y2] == "_":
            return True # Valid move for Â
        return True

    def capture_pieces(self, x, y):
        # Check and capture any pieces sandwiched orthogonally
        opponent = "A" if self.current_player == 1 else "V"
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            mx, my = x + 2 * dx, y + 2 * dy
            if 0 <= nx < 7 and 0 <= ny < 7 and 0 <= mx < 7 and 0 <= my < 7:
                if self.board[nx][ny] == opponent and self.board[mx][my] == self.board[x][y]:
                    self.board[nx][ny] = "_"  # Capture the piece

    def check_win_conditions(self):
        # Check if any win condition has been met
        for x in range(7):
            for y in range(7):
                if self.board[x][y] == "Â":
                    # Player 2 wins if Â is on the border
                    if x == 0 or x == 6 or y == 0 or y == 6:
                        print("Player 2 wins! Â reached the border.")
                        self.game_over = True
                        return
                    # Player 1 wins if Â is captured
                    if self.board[x][y] == "_":
                        print("Player 1 wins! Â was captured.")
                        self.game_over = True
                        return

    def make_move(self, x1, y1, x2, y2):
        # Attempt to make a move
        if not self.is_valid_move(x1, y1, x2, y2):
            print("Invalid move. Try again.")
            return False
        # Move the piece
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = "_"
        # Check for captures
        self.capture_pieces(x2, y2)
        # Check for win conditions
        self.check_win_conditions()
        # Switch player
        self.current_player = 2 if self.current_player == 1 else 1
        return True

    def play(self):
        # Main game loop
        print("Welcome to Lilac!")
        self.display_board()
        while not self.game_over:
            print(f"Player {self.current_player}'s turn.")
            try:
                x1, y1, x2, y2 = map(int, input("Enter your move (x1 y1 x2 y2): ").split())
                if self.make_move(x1, y1, x2, y2):
                    self.display_board()
            except ValueError:
                print("Invalid input. Enter four integers separated by spaces.")
        print("Game over!")


# Run the game
if __name__ == "__main__":
    game = LilacGame()
    game.play()