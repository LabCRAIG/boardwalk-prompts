
class Reversi:
    def __init__(self):
        # Initialize the board with 8x8 size
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        # Starting positions
        self.board[3][3], self.board[4][4] = "W", "W"
        self.board[3][4], self.board[4][3] = "B", "B"
        self.current_player = "B"  # Black starts

    def display_board(self):
        print("  " + " ".join(map(str, range(8))))
        for i, row in enumerate(self.board):
            print(i, " ".join(row))
        print()

    def is_valid_move(self, row, col):
        # Check if the position is within bounds
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
        # Check if the position is empty
        if self.board[row][col] != " ":
            return False
        # Check if the position is in a restricted 2x2 corner
        if (row, col) in [
            (0, 0), (0, 1), (1, 0), (1, 1),
            (0, 6), (0, 7), (1, 6), (1, 7),
            (6, 0), (6, 1), (7, 0), (7, 1),
            (6, 6), (6, 7), (7, 6), (7, 7),
        ]:
            return False
        # Check if placing the piece flips at least one opponent piece
        return self.check_directions(row, col)

    def check_directions(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        opponent = "W" if self.current_player == "B" else "B"
        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == opponent:
                    found_opponent = True
                elif self.board[r][c] == self.current_player and found_opponent:
                    return True
                else:
                    break
                r += dr
                c += dc
        return False

    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            print("Invalid move. Try again.")
            return False
        # Place the piece
        self.board[row][col] = self.current_player
        # Flip opponent pieces
        self.flip_pieces(row, col)
        # Switch turns
        self.current_player = "W" if self.current_player == "B" else "B"
        return True

    def flip_pieces(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        opponent = "W" if self.current_player == "B" else "B"
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == opponent:
                    pieces_to_flip.append((r, c))
                elif self.board[r][c] == self.current_player:
                    for flip_r, flip_c in pieces_to_flip:
                        self.board[flip_r][flip_c] = self.current_player
                    break
                else:
                    break
                r += dr
                c += dc

    def has_valid_moves(self):
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    return True
        return False

    def play_game(self):
        print("Welcome to Reversi!")
        self.display_board()
        while self.has_valid_moves():
            print(f"Player {self.current_player}'s turn")
            try:
                row, col = map(int, input("Enter row and column (e.g., 3 4): ").split())
                if self.make_move(row, col):
                    self.display_board()
                else:
                    continue
            except ValueError:
                print("Invalid input. Please enter row and column as integers.")
        # Determine winner
        black_count = sum(row.count("B") for row in self.board)
        white_count = sum(row.count("W") for row in self.board)
        print("Game over!")
        print(f"Black: {black_count}, White: {white_count}")
        if black_count > white_count:
            print("Black wins!")
        elif white_count > black_count:
            print("White wins!")
        else:
            print("It's a tie!")


# Play the game
if __name__ == "__main__":
    game = Reversi()
    game.play_game()
