
class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def print_board(self):
        print("  0 1 2")
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))
        print()

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            if self.check_win():
                self.print_board()
                print(f"Player {self.current_player} wins!")
                return True
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return False
        else:
            print("Invalid move. Try again.")
            return False

    def check_win(self):
        # Check rows and columns
        for i in range(3):
            if all(self.board[i][j] == self.current_player for j in range(3)):  # Row
                return True
            if all(self.board[j][i] == self.current_player for j in range(3)):  # Column
                return True

        # Check 2x2 squares
        for i in range(2):  # Only top-left corners of 2x2 squares are valid
            for j in range(2):
                if (self.board[i][j] == self.current_player and
                    self.board[i][j+1] == self.current_player and
                    self.board[i+1][j] == self.current_player and
                    self.board[i+1][j+1] == self.current_player):
                    return True

        return False

    def is_full(self):
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))

    def play(self):
        print("Welcome to Tic-Tac-Toe!")
        print("Victory condition: Rows, columns, or a 2x2 square filled with your marks.")
        self.print_board()
        while not self.is_full():
            print(f"Player {self.current_player}'s turn.")
            try:
                row, col = map(int, input("Enter row and column (e.g., 0 1): ").split())
                if self.make_move(row, col):
                    break
            except (ValueError, IndexError):
                print("Invalid input. Enter row and column as two numbers between 0 and 2.")
        else:
            print("It's a draw!")


# Run the game
if __name__ == "__main__":
    game = TicTacToe()
    game.play()
