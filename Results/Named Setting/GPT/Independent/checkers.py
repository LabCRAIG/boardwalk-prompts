
class CheckersGame:
    def __init__(self):
        self.board = self.create_board()
        self.turn = 'black'  # Black starts first

    def create_board(self):
        board = [[' ' for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        board[row][col] = 'b'  # Black pieces
                    elif row > 4:
                        board[row][col] = 'r'  # Red pieces
        return board

    def print_board(self):
        print("  " + " ".join(str(i) for i in range(8)))
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))

    def is_valid_move(self, start, end):
        sx, sy = start
        ex, ey = end
        if ex < 0 or ex >= 8 or ey < 0 or ey >= 8:
            return False  # Move is out of bounds
        if self.board[ex][ey] != ' ':
            return False  # Destination is not empty
        piece = self.board[sx][sy]
        if piece.lower() != self.turn[0]:
            return False  # Not the right player's turn
        if abs(ex - sx) != 1 or abs(ey - sy) != 1:
            return False  # Move must be diagonal by 1 space
        return True

    def is_valid_capture(self, start, end):
        sx, sy = start
        ex, ey = end
        if ex < 0 or ex >= 8 or ey < 0 or ey >= 8:
            return False  # Move is out of bounds
        if self.board[ex][ey] != ' ':
            return False  # Destination is not empty
        piece = self.board[sx][sy]
        if piece.lower() != self.turn[0]:
            return False  # Not the right player's turn
        if abs(ex - sx) != 2 or abs(ey - sy) != 2:
            return False  # Capture must be diagonal by 2 spaces
        mid_x, mid_y = (sx + ex) // 2, (sy + ey) // 2
        mid_piece = self.board[mid_x][mid_y]
        if mid_piece == ' ' or mid_piece.lower() == self.turn[0]:
            return False  # No opponent piece to capture
        return True

    def move_piece(self, start, end):
        if self.is_valid_move(start, end):
            sx, sy = start
            ex, ey = end
            self.board[ex][ey] = self.board[sx][sy]
            self.board[sx][sy] = ' '
            self.check_king(ex, ey)
            self.change_turn()
        elif self.is_valid_capture(start, end):
            sx, sy = start
            ex, ey = end
            mid_x, mid_y = (sx + ex) // 2, (sy + ey) // 2
            self.board[ex][ey] = self.board[sx][sy]
            self.board[sx][sy] = ' '
            self.board[mid_x][mid_y] = ' '
            self.check_king(ex, ey)
            if not self.can_capture((ex, ey)):
                self.change_turn()
        else:
            print("Invalid move. Try again.")

    def check_king(self, x, y):
        if self.board[x][y] == 'b' and x == 7:
            self.board[x][y] = 'B'  # Black piece becomes a king
        elif self.board[x][y] == 'r' and x == 0:
            self.board[x][y] = 'R'  # Red piece becomes a king

    def can_capture(self, position):
        x, y = position
        piece = self.board[x][y]
        if piece.lower() != self.turn[0]:
            return False
        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        for dx, dy in directions:
            ex, ey = x + dx, y + dy
            if self.is_valid_capture((x, y), (ex, ey)):
                return True
        return False

    def change_turn(self):
        self.turn = 'red' if self.turn == 'black' else 'black'

    def is_game_over(self):
        black_pieces = sum(row.count('b') + row.count('B') for row in self.board)
        red_pieces = sum(row.count('r') + row.count('R') for row in self.board)
        return black_pieces == 0 or red_pieces == 0

    def play(self):
        while not self.is_game_over():
            self.print_board()
            print(f"{self.turn.capitalize()}'s turn")
            try:
                start = tuple(map(int, input("Enter the start position (row col): ").split()))
                end = tuple(map(int, input("Enter the end position (row col): ").split()))
                self.move_piece(start, end)
            except ValueError:
                print("Invalid input. Please enter row and column as integers.")
        self.print_board()
        print("Game over!")
        winner = 'Red' if self.turn == 'black' else 'Black'
        print(f"{winner} wins!")


# To play the game, create an instance of the game and call the play method:
if __name__ == "__main__":
    game = CheckersGame()
    game.play()
