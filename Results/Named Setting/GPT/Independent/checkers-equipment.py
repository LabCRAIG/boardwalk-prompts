
class CheckersGame:
    def __init__(self):
        self.board_size = 8
        self.board = self.initialize_board()
        self.current_player = "X"  # Player X starts
        self.piece_symbols = {"X": "X", "O": "O"}  # Player pieces

    def initialize_board(self):
        """
        Initializes the board with pieces on both sides.
        Each player occupies the first two rows closest to them.
        """
        board = [[" " for _ in range(self.board_size)] for _ in range(self.board_size)]
        for row in range(2):  # Player X pieces
            for col in range(self.board_size):
                board[row][col] = "X"
        for row in range(self.board_size - 2, self.board_size):  # Player O pieces
            for col in range(self.board_size):
                board[row][col] = "O"
        return board

    def print_board(self):
        """
        Prints the current state of the board.
        """
        for row in self.board:
            print(" | ".join(row))
            print("-" * (self.board_size * 4 - 3))

    def valid_move(self, start, end):
        """
        Validates if a move from start to end is valid.
        """
        start_row, start_col = start
        end_row, end_col = end
        if not (0 <= start_row < self.board_size and 0 <= start_col < self.board_size):
            return False
        if not (0 <= end_row < self.board_size and 0 <= end_col < self.board_size):
            return False

        piece = self.board[start_row][start_col]
        if piece != self.current_player:
            return False

        if self.board[end_row][end_col] != " ":
            return False

        dx = end_row - start_row
        dy = abs(end_col - start_col)
        if dx == 1 and dy == 1:  # Regular forward move
            if self.current_player == "X" and dx > 0:
                return True
            elif self.current_player == "O" and dx < 0:
                return True
        elif dx == 2 and dy == 2:  # Jump move
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            if self.board[mid_row][mid_col] == self.piece_symbols["X" if self.current_player == "O" else "O"]:
                self.board[mid_row][mid_col] = " "  # Capture the opponent's piece
                return True

        return False

    def make_move(self, start, end):
        """
        Makes a move if valid.
        """
        if self.valid_move(start, end):
            start_row, start_col = start
            end_row, end_col = end
            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = " "
            self.switch_player()
            return True
        else:
            print("Invalid move. Try again.")
            return False

    def switch_player(self):
        """
        Switches the current player.
        """
        self.current_player = "X" if self.current_player == "O" else "O"

    def is_game_over(self):
        """
        Checks if the game is over (one side has no pieces left).
        """
        x_pieces = sum(row.count("X") for row in self.board)
        o_pieces = sum(row.count("O") for row in self.board)
        if x_pieces == 0:
            print("Player O wins!")
            return True
        elif o_pieces == 0:
            print("Player X wins!")
            return True
        return False

    def play_game(self):
        """
        Main game loop.
        """
        print("Welcome to Checkers!")
        while not self.is_game_over():
            self.print_board()
            print(f"Player {self.current_player}'s turn.")
            try:
                start = tuple(map(int, input("Enter start position (row col): ").split()))
                end = tuple(map(int, input("Enter end position (row col): ").split()))
                self.make_move(start, end)
            except ValueError:
                print("Invalid input. Please enter row and column as integers separated by a space.")

if __name__ == "__main__":
    game = CheckersGame()
    game.play_game()
