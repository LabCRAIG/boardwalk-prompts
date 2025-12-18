
class PegSolitaireDiamond:
    def __init__(self, size=5):
        """
        Initialize the diamond-shaped Peg Solitaire board.
        The board size determines the height of the diamond (e.g., 5 for a 5x5 diamond).

        :param size: Height of the diamond shape.
        """
        if size < 3 or size % 2 == 0:
            raise ValueError("Size must be an odd number greater than or equal to 3.")
        self.size = size
        self.board = self.create_diamond_board(size)
        self.center = (size // 2, size // 2)  # Center of the diamond

    def create_diamond_board(self, size):
        """
        Create the diamond-shaped board filled with pegs (1).
        The center of the board starts with an empty space (0).

        :param size: Height of the diamond shape.
        :return: 2D list representing the board.
        """
        board = []
        mid = size // 2
        for i in range(size):
            row = []
            for j in range(size):
                if abs(mid - i) + abs(mid - j) <= mid:
                    row.append(1)  # Peg
                else:
                    row.append(None)  # Invalid position
            board.append(row)
        board[mid][mid] = 0  # Empty center
        return board

    def display_board(self):
        """
        Print the board in a human-readable format.
        """
        for row in self.board:
            print(" ".join(["." if cell is None else "O" if cell == 1 else "_" for cell in row]))
        print()

    def is_valid_move(self, start, end):
        """
        Check if the move from start to end is valid.

        :param start: Tuple (x, y) of the start position.
        :param end: Tuple (x, y) of the end position.
        :return: True if the move is valid, False otherwise.
        """
        x1, y1 = start
        x2, y2 = end

        # Check if start and end positions are within bounds and valid
        if not (0 <= x1 < self.size and 0 <= y1 < self.size) or not (0 <= x2 < self.size and 0 <= y2 < self.size):
            return False
        if self.board[x1][y1] != 1 or self.board[x2][y2] != 0:
            return False

        # Check if the move is exactly two spaces away in a straight line
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) + abs(dy) != 2 or (dx != 0 and dy != 0):
            return False

        # Check if there is a peg in the middle position
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        if self.board[mid_x][mid_y] != 1:
            return False

        return True

    def make_move(self, start, end):
        """
        Perform a move if it is valid.

        :param start: Tuple (x, y) of the start position.
        :param end: Tuple (x, y) of the end position.
        :return: True if the move was successful, False otherwise.
        """
        if self.is_valid_move(start, end):
            x1, y1 = start
            x2, y2 = end
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2

            # Make the move: remove the peg at start and middle, place peg at end
            self.board[x1][y1] = 0
            self.board[mid_x][mid_y] = 0
            self.board[x2][y2] = 1
            return True
        return False

    def has_moves_left(self):
        """
        Check if there are any valid moves left on the board.

        :return: True if there are valid moves left, False otherwise.
        """
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 1:
                    # Check all possible moves from this position
                    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        if self.is_valid_move((x, y), (x + dx, y + dy)):
                            return True
        return False

    def play(self):
        """
        Allow the user to play the game interactively.
        """
        print("Welcome to Peg Solitaire (Diamond Board)!")
        self.display_board()

        while self.has_moves_left():
            try:
                start = tuple(map(int, input("Enter the start position (row col): ").split()))
                end = tuple(map(int, input("Enter the end position (row col): ").split()))
                if self.make_move(start, end):
                    print("Move successful!")
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter two integers separated by a space.")

            self.display_board()

        print("No more moves left! Game over.")


# Run the game
if __name__ == "__main__":
    game = PegSolitaireDiamond(size=5)  # Create a diamond board of size 5
    game.play()
