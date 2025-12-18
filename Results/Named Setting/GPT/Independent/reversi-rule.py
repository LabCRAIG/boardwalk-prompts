
class Reversi:
    def __init__(self):
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        self.board[3][3], self.board[3][4] = "W", "B"
        self.board[4][3], self.board[4][4] = "B", "W"
        self.current_player = "B"
        self.king_used = {"B": False, "W": False}  # Track if each player has used their king

    def display_board(self):
        print("  " + " ".join(map(str, range(8))))
        for i, row in enumerate(self.board):
            print(str(i) + " " + " ".join(row))

    def is_valid_move(self, row, col, is_king):
        if self.board[row][col] != " ":
            return False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            has_opponent_piece = False
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] not in (" ", self.current_player, self.get_king(self.current_player)):
                has_opponent_piece = True
                r += dr
                c += dc
            if has_opponent_piece and 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == (self.current_player if not is_king else self.get_king(self.current_player)):
                return True
        return False

    def get_valid_moves(self):
        valid_moves = []
        for r in range(8):
            for c in range(8):
                if self.is_valid_move(r, c, is_king=False) or (not self.king_used[self.current_player] and self.is_valid_move(r, c, is_king=True)):
                    valid_moves.append((r, c))
        return valid_moves

    def make_move(self, row, col, is_king):
        if not self.is_valid_move(row, col, is_king):
            print("Invalid move. Try again.")
            return False

        self.board[row][col] = self.get_king(self.current_player) if is_king else self.current_player
        if is_king:
            self.king_used[self.current_player] = True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] not in (" ", self.current_player, self.get_king(self.current_player)):
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                for rr, cc in pieces_to_flip:
                    self.board[rr][cc] = self.current_player

        self.current_player = "W" if self.current_player == "B" else "B"
        return True

    def get_king(self, player):
        return "K" + player

    def has_valid_moves(self):
        return bool(self.get_valid_moves())

    def count_pieces(self):
        b_count = sum(row.count("B") + row.count("KB") for row in self.board)
        w_count = sum(row.count("W") + row.count("KW") for row in self.board)
        return b_count, w_count

    def play_game(self):
        while True:
            self.display_board()
            print(f"{self.current_player}'s turn")
            print(f"Available moves: {self.get_valid_moves()}")
            if not self.has_valid_moves():
                print(f"No valid moves for {self.current_player}. Turn skipped.")
                self.current_player = "W" if self.current_player == "B" else "B"
                if not self.has_valid_moves():
                    break
                continue

            move = input("Enter your move (row, col) or 'K' for king move: ").strip()
            if move.lower() == "k" and not self.king_used[self.current_player]:
                row, col = map(int, input("Enter the position for your king (row, col): ").split(","))
                if not self.make_move(row, col, is_king=True):
                    continue
            else:
                try:
                    row, col = map(int, move.split(","))
                    if not self.make_move(row, col, is_king=False):
                        continue
                except ValueError:
                    print("Invalid input. Try again.")
                    continue

        b_count, w_count = self.count_pieces()
        print("Game over!")
        print(f"Black: {b_count}, White: {w_count}")
        if b_count > w_count:
            print("Black wins!")
        elif w_count > b_count:
            print("White wins!")
        else:
            print("It's a tie!")


if __name__ == "__main__":
    game = Reversi()
    game.play_game()
