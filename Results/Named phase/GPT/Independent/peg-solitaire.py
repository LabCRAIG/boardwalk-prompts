
class PegSolitaire:
    def __init__(self):
        # Initialize the board with a standard cross-shaped configuration
        self.board = [
            [" ", " ", "X", "X", "X", " ", " "],
            [" ", " ", "X", "X", "X", " ", " "],
            ["X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "O", "X", "X", "X"],  # 'O' is the empty hole
            ["X", "X", "X", "X", "X", "X", "X"],
            [" ", " ", "X", "X", "X", " ", " "],
            [" ", " ", "X", "X", "X", " ", " "],
        ]

    def display_board(self):
        # Print the board to the console
        for row in self.board:
            print(" ".join(row))
        print()

    def is_valid_move(self, x1, y1, x2, y2):
        # Check if the move is valid
        if x2 < 0 or x2 >= 7 or y2 < 0 or y2 >= 7:
            return False  # Destination is out of bounds
        if self.board[x1][y1] != "X" or self.board[x2][y2] != "O":
            return False  # Starting position must have a peg, and destination must be empty
        if abs(x1 - x2) == 2 and y1 == y2:
            # Horizontal move
            mid_x = (x1 + x2) // 2
            if self.board[mid_x][y1] == "X":
                return True
        elif abs(y1 - y2) == 2 and x1 == x2:
            # Vertical move
            mid_y = (y1 + y2) // 2
            if self.board[x1][mid_y] == "X":
                return True
        return False

    def make_move(self, x1, y1, x2, y2):
        # Execute the move if it's valid
        if self.is_valid_move(x1, y1, x2, y2):
            self.board[x1][y1] = "O"  # Remove the peg from the starting position
            self.board[x2][y2] = "X"  # Place the peg in the destination
            # Remove the jumped-over peg
            if x1 == x2:
                self.board[x1][(y1 + y2) // 2] = "O"
            else:
                self.board[(x1 + x2) // 2][y1] = "O"
            return True
        else:
            print("Invalid move! Try again.")
            return False

    def has_moves_left(self):
        # Check if there are any valid moves left
        for x in range(7):
            for y in range(7):
                if self.board[x][y] == "X":
                    # Check all possible moves from this position
                    if (
                        self.is_valid_move(x, y, x + 2, y)
                        or self.is_valid_move(x, y, x - 2, y)
                        or self.is_valid_move(x, y, x, y + 2)
                        or self.is_valid_move(x, y, x, y - 2)
                    ):
                        return True
        return False

    def count_pegs(self):
        # Count the remaining pegs on the board
        return sum(row.count("X") for row in self.board)

    def play(self):
        # Main game loop
        print("Welcome to Peg Solitaire!")
        print("The board positions are indexed from 0 to 6.")
        print("Input your moves in the format: x1 y1 x2 y2")
        print("Where (x1, y1) is the starting position and (x2, y2) is the destination.\n")

        while self.has_moves_left():
            self.display_board()
            print(f"Remaining pegs: {self.count_pegs()}")
            try:
                x1, y1, x2, y2 = map(int, input("Enter your move: ").split())
                self.make_move(x1, y1, x2, y2)
            except ValueError:
                print("Invalid input! Please enter four integers separated by spaces.")

        self.display_board()
        remaining_pegs = self.count_pegs()
        print(f"Game over! You have {remaining_pegs} peg(s) remaining.")
        if remaining_pegs == 1:
            print("Congratulations, you solved the puzzle!")
        else:
            print("Better luck next time!")


# Run the game
if __name__ == "__main__":
    game = PegSolitaire()
    game.play()
