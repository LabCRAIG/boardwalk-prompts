
# Python implementation of Checkers with a special rule for king capturing

class CheckersGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_turn = 'W'  # 'W' for White, 'B' for Black

    def initialize_board(self):
        # Initialize an 8x8 board with pieces in starting positions
        board = [[' ' for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 != 0:  # Pieces are on black squares
                    if i < 3:
                        board[i][j] = 'B'  # Black piece
                    elif i > 4:
                        board[i][j] = 'W'  # White piece
        return board

    def print_board(self):
        print("  A B C D E F G H")
        for i in range(8):
            print(f"{8 - i} " + " ".join(self.board[i]) + f" {8 - i}")
        print("  A B C D E F G H")

    def is_valid_move(self, start, end):
        # Basic validation for moves
        sx, sy = start
        ex, ey = end
        if not (0 <= sx < 8 and 0 <= sy < 8 and 0 <= ex < 8 and 0 <= ey < 8):
            return False  # Out of bounds
        if self.board[sx][sy].upper() != self.current_turn:
            return False  # Wrong player's turn
        if self.board[ex][ey] != ' ':
            return False  # End position not empty
        return True

    def make_move(self, start, end):
        sx, sy = start
        ex, ey = end
        piece = self.board[sx][sy]

        # Check if it is a capture
        if abs(ex - sx) == 2 and abs(ey - sy) == 2:
            mx, my = (sx + ex) // 2, (sy + ey) // 2  # Middle piece coordinates
            middle_piece = self.board[mx][my]
            if middle_piece.upper() != self.current_turn and middle_piece != ' ':
                # Special rule: if both are kings, remove both
                if piece.isupper() and middle_piece.isupper():
                    self.board[sx][sy] = ' '
                    self.board[mx][my] = ' '
                else:
                    self.board[sx][sy] = ' '
                    self.board[mx][my] = ' '
                    self.board[ex][ey] = piece
                self.check_promotion(ex, ey)
                self.switch_turn()
                return True
        elif abs(ex - sx) == 1 and abs(ey - sy) == 1:
            # Regular move
            self.board[sx][sy] = ' '
            self.board[ex][ey] = piece
            self.check_promotion(ex, ey)
            self.switch_turn()
            return True

        return False

    def check_promotion(self, x, y):
        # Promote to king if reaching the last row
        piece = self.board[x][y]
        if piece == 'W' and x == 0:
            self.board[x][y] = 'K'
        elif piece == 'B' and x == 7:
            self.board[x][y] = 'Q'

    def switch_turn(self):
        self.current_turn = 'B' if self.current_turn == 'W' else 'W'

    def parse_position(self, pos):
        # Translate chess-like positions (e.g., A3) to board indices
        col, row = pos
        x = 8 - int(row)
        y = ord(col.upper()) - ord('A')
        return x, y

    def play(self):
        while True:
            self.print_board()
            print(f"{self.current_turn}'s turn")
            start = input("Enter the piece to move (e.g., A3): ").strip()
            end = input("Enter the destination (e.g., B4): ").strip()

            try:
                start_pos = self.parse_position(start)
                end_pos = self.parse_position(end)

                if self.is_valid_move(start_pos, end_pos):
                    if self.make_move(start_pos, end_pos):
                        continue
                print("Invalid move. Try again.")
            except Exception as e:
                print(f"Error: {e}. Try again.")
