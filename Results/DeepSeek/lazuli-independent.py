class Lazuli:
    def __init__(self):
        # Initialize the board
        self.board = [['.' for _ in range(7)] for _ in range(7)]
        for i in range(7):
            for j in range(7):
                # Nullify the 2x2 corners
                if (i < 2 and j < 2) or (i < 2 and j > 4) or (i > 4 and j < 2) or (i > 4 and j > 4):
                    self.board[i][j] = '.'
                else:
                    self.board[i][j] = 'X'
        # Empty the center
        self.board[3][3] = ' '

    def __str__(self):
        # Display the board with row/column labels
        s = "  0 1 2 3 4 5 6\n"
        for i in range(7):
            s += f"{i} "
            for j in range(7):
                s += self.board[i][j] + " "
            s += "\n"
        return s

    def is_valid_move(self, x1, y1, x2, y2):
        # Check if the move is valid
        if not (0 <= x1 < 7 and 0 <= y1 < 7 and 0 <= x2 < 7 and 0 <= y2 < 7):
            return False
        if self.board[x1][y1] != 'X' or self.board[x2][y2] != ' ':
            return False
        # Check if it's a jump over one piece horizontally or vertically
        if abs(x1 - x2) == 2 and y1 == y2:  # Vertical jump
            mid_x = (x1 + x2) // 2
            if self.board[mid_x][y1] == 'X':
                return True
        elif abs(y1 - y2) == 2 and x1 == x2:  # Horizontal jump
            mid_y = (y1 + y2) // 2
            if self.board[x1][mid_y] == 'X':
                return True
        return False

    def make_move(self, x1, y1, x2, y2):
        if self.is_valid_move(x1, y1, x2, y2):
            # Move the piece
            self.board[x1][y1] = ' '
            self.board[x2][y2] = 'X'
            # Remove the jumped piece
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            self.board[mid_x][mid_y] = ' '
            return True
        return False

    def check_win(self):
        # Count remaining pieces
        pieces = sum(row.count('X') for row in self.board)
        return pieces == 1 and self.board[3][3] == 'X'

    def check_loss(self):
        # Check if no valid moves left
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 'X':
                    # Check all possible jumps
                    for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                        x2, y2 = i + dx, j + dy
                        if 0 <= x2 < 7 and 0 <= y2 < 7:
                            if self.is_valid_move(i, j, x2, y2):
                                return False
        return True

    def play(self):
        print("Welcome to Lazuli!")
        print("Move pieces by jumping over them (e.g., '3 1 -> 3 3')")
        print("Goal: End with one piece in the center.")
        print(self)
        
        while True:
            if self.check_win():
                print("Congratulations! You won!")
                break
            if self.check_loss():
                print("No valid moves left. You lost!")
                break
            
            try:
                move = input("Enter your move (x1 y1 -> x2 y2): ").strip()
                if '->' not in move:
                    raise ValueError("Invalid move format.")
                start, end = move.split('->')
                x1, y1 = map(int, start.strip().split())
                x2, y2 = map(int, end.strip().split())
                
                if self.make_move(x1, y1, x2, y2):
                    print(self)
                else:
                    print("Invalid move. Try again.")
            except Exception as e:
                print(f"Error: {e}. Please enter moves like '3 1 -> 3 3'.")

if __name__ == "__main__":
    game = Lazuli()
    game.play()