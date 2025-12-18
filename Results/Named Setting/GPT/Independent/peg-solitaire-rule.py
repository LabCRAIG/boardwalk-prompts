
class PegSolitaire:
    def __init__(self):
        # Initialize the board
        # 0: Empty space, 1: Peg, -1: Invalid space
        self.board = [
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [1,  1,  1, 1, 1,  1,  1],
            [1,  1,  1, 0, 1,  1,  1],
            [1,  1,  1, 1, 1,  1,  1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
        ]

    def display_board(self):
        # Display the board in a readable format
        for row in self.board:
            print(" ".join(str(cell) if cell != -1 else " " for cell in row))
        print()

    def is_valid_move(self, x1, y1, x2, y2):
        # Check if a move from (x1, y1) to (x2, y2) is valid
        if not (0 <= x1 < 7 and 0 <= y1 < 7 and 0 <= x2 < 7 and 0 <= y2 < 7):
            return False
        if self.board[x1][y1] != 1 or self.board[x2][y2] != 0:
            return False
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) == 2 and dy == 0 and self.board[x1 + dx // 2][y1] == 1:
            return True
        if abs(dy) == 2 and dx == 0 and self.board[x1][y1 + dy // 2] == 1:
            return True
        return False

    def make_move(self, x1, y1, x2, y2):
        # Make a move if it's valid
        if self.is_valid_move(x1, y1, x2, y2):
            dx, dy = x2 - x1, y2 - y1
            self.board[x1][y1] = 0
            self.board[x1 + dx // 2][y1 + dy // 2] = 0
            self.board[x2][y2] = 1
            return True
        return False

    def count_pegs(self):
        # Count the number of remaining pegs
        return sum(row.count(1) for row in self.board)

    def is_game_won(self):
        # Check if the game is won (two pegs left and one cannot capture the other)
        pegs = [(x, y) for x in range(7) for y in range(7) if self.board[x][y] == 1]
        if len(pegs) != 2:
            return False
        (x1, y1), (x2, y2) = pegs
        return not self.is_valid_move(x1, y1, x2, y2) and not self.is_valid_move(x2, y2, x1, y1)

    def is_game_over(self):
        # Check if the game is over (no valid moves left)
        for x in range(7):
            for y in range(7):
                if self.board[x][y] == 1:
                    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        if self.is_valid_move(x, y, x + dx, y + dy):
                            return False
        return True

    def play(self):
        # Main game loop
        while True:
            self.display_board()
            if self.is_game_won():
                print("You won the game!")
                break
            if self.is_game_over():
                print("Game over. No valid moves left.")
                break
            try:
                x1, y1, x2, y2 = map(int, input("Enter your move (x1 y1 x2 y2): ").split())
                if not self.make_move(x1, y1, x2, y2):
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter four integers.")


if __name__ == "__main__":
    game = PegSolitaire()
    game.play()
