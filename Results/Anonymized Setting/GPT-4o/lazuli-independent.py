class Lazuli:
    def __init__(self):
        # Initialize the 7x7 board according to the rules
        self.board = [
            [None, None, "X", "X", "X", None, None],
            [None, None, "X", "X", "X", None, None],
            ["X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", None, "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X"],
            [None, None, "X", "X", "X", None, None],
            [None, None, "X", "X", "X", None, None],
        ]
        self.rows = 7
        self.cols = 7

    def display(self):
        # Print the board in a readable format
        print("\n  " + " ".join(str(i) for i in range(self.cols)))
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(cell if cell else "." for cell in row))

    def is_valid_move(self, start, end):
        # Check if a move is valid
        sx, sy = start
        ex, ey = end

        # Ensure the start and end positions are within bounds
        if not (0 <= sx < self.rows and 0 <= sy < self.cols and 0 <= ex < self.rows and 0 <= ey < self.cols):
            return False

        # The start position must have an "X" piece
        if self.board[sx][sy] != "X":
            return False

        # The end position must be empty
        if self.board[ex][ey] is not None:
            return False

        # Determine the position of the piece being jumped over
        mx, my = (sx + ex) // 2, (sy + ey) // 2

        # Check if the move is horizontal or vertical and spans exactly 2 cells
        if abs(sx - ex) == 2 and sy == ey:  # Vertical move
            return self.board[mx][my] == "X"
        elif abs(sy - ey) == 2 and sx == ex:  # Horizontal move
            return self.board[mx][my] == "X"

        # Invalid move otherwise
        return False

    def make_move(self, start, end):
        # Perform the move on the board
        if self.is_valid_move(start, end):
            sx, sy = start
            ex, ey = end
            mx, my = (sx + ex) // 2, (sy + ey) // 2

            # Move the piece
            self.board[sx][sy] = None
            self.board[mx][my] = None
            self.board[ex][ey] = "X"
            return True
        else:
            return False

    def has_moves_left(self):
        # Check if there are any valid moves left
        for x in range(self.rows):
            for y in range(self.cols):
                if self.board[x][y] == "X":
                    # Check all possible moves from this position
                    possible_moves = [
                        ((x, y), (x + 2, y)),  # Down
                        ((x, y), (x - 2, y)),  # Up
                        ((x, y), (x, y + 2)),  # Right
                        ((x, y), (x, y - 2)),  # Left
                    ]
                    for start, end in possible_moves:
                        if self.is_valid_move(start, end):
                            return True
        return False

    def is_win(self):
        # Check if the player has won
        remaining_pieces = sum(row.count("X") for row in self.board)
        return remaining_pieces == 1 and self.board[3][3] == "X"

    def play(self):
        # Main game loop
        print("Welcome to Lazuli! Make moves to capture pieces and win by having only one piece left in the center.")
        while True:
            self.display()
            if self.is_win():
                print("Congratulations! You win!")
                break
            if not self.has_moves_left():
                print("No moves left. You lose!")
                break

            # Get player input for the move
            try:
                start = tuple(map(int, input("Enter the starting position (row col): ").split()))
                end = tuple(map(int, input("Enter the ending position (row col): ").split()))
                if not self.make_move(start, end):
                    print("Invalid move. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Enter row and column as two integers separated by a space.")


# Run the game
if __name__ == "__main__":
    game = Lazuli()
    game.play()