class Quartz:
    def __init__(self):
        # Initialize an 8x8 board with the center occupied as per rules
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'A'
        self.board[3][4] = 'V'
        self.board[4][3] = 'V'
        self.board[4][4] = 'A'
        self.current_player = 'A'  # Player 1 starts with 'A'

    def print_board(self):
        print("  " + " ".join(str(i) for i in range(8)))
        for i, row in enumerate(self.board):
            print(i, " ".join(row))
        print()

    def is_valid_move(self, row, col, player):
        if self.board[row][col] != ' ':
            return False  # The space is not empty
        opponent = 'A' if player == 'V' else 'V'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False

            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == opponent:
                    found_opponent = True
                elif self.board[r][c] == player:
                    if found_opponent:
                        return True
                    else:
                        break
                else:
                    break
                r += dr
                c += dc

        return False

    def make_move(self, row, col, player):
        if not self.is_valid_move(row, col, player):
            return False  # Invalid move

        self.board[row][col] = player
        opponent = 'A' if player == 'V' else 'V'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []

            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == opponent:
                    pieces_to_flip.append((r, c))
                elif self.board[r][c] == player:
                    for rr, cc in pieces_to_flip:
                        self.board[rr][cc] = player
                    break
                else:
                    break
                r += dr
                c += dc

        return True

    def has_valid_moves(self, player):
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, player):
                    return True
        return False

    def count_pieces(self):
        count_a = sum(row.count('A') for row in self.board)
        count_v = sum(row.count('V') for row in self.board)
        return count_a, count_v

    def play_game(self):
        while True:
            self.print_board()
            if not self.has_valid_moves(self.current_player):
                print(f"Player {self.current_player} has no valid moves and must pass.")
                self.current_player = 'A' if self.current_player == 'V' else 'V'
                if not self.has_valid_moves(self.current_player):
                    print("No valid moves left for either player. Game over!")
                    break
                continue

            print(f"Player {self.current_player}'s turn.")
            try:
                row, col = map(int, input("Enter row and column to place your piece (e.g., '3 4'): ").split())
                if self.make_move(row, col, self.current_player):
                    self.current_player = 'A' if self.current_player == 'V' else 'V'
                else:
                    print("Invalid move. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter row and column as two integers between 0 and 7.")

        count_a, count_v = self.count_pieces()
        print("Final board:")
        self.print_board()
        print(f"Player A (A) has {count_a} pieces.")
        print(f"Player V (V) has {count_v} pieces.")
        if count_a > count_v:
            print("Player A wins!")
        elif count_v > count_a:
            print("Player V wins!")
        else:
            print("It's a tie!")


if __name__ == "__main__":
    game = Quartz()
    game.play_game()
