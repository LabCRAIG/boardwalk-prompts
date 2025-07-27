class LilacGame:
    def __init__(self):
        # Initialize the 7x7 board
        self.board = [
            ['_', 'V', 'V', 'V', '_', '_', '_'],
            ['_', '_', '_', 'V', '_', '_', '_'],
            ['V', '_', 'A', 'A', 'A', '_', 'V'],
            ['V', 'V', 'A', 'Â', 'A', 'V', 'V'],
            ['V', '_', 'A', 'A', 'A', '_', 'V'],
            ['_', '_', '_', 'V', '_', '_', '_'],
            ['_', 'V', 'V', 'V', '_', '_', '_']
        ]
        self.current_player = 1  # Player 1 starts
        self.game_over = False
        self.winner = None

    def print_board(self):
        print("\nCurrent Board:")
        for row in self.board:
            print(" ".join(piece if piece != '_' else '_' for piece in row))
        print()

    def is_valid_position(self, x, y):
        return 0 <= x < 7 and 0 <= y < 7

    def is_owned_by_current_player(self, x, y):
        piece = self.board[x][y]
        if self.current_player == 1:
            return piece == 'V'
        else:
            return piece == 'A' or piece == 'Â'

    def is_center(self, x, y):
        return x == 3 and y == 3

    def is_border(self, x, y):
        return x == 0 or x == 6 or y == 0 or y == 6

    def move_piece(self, from_x, from_y, to_x, to_y):
        # Check if game is already over
        if self.game_over:
            print("Game is already over!")
            return False

        # Check if source is valid
        if not self.is_valid_position(from_x, from_y) or not self.is_valid_position(to_x, to_y):
            print("Invalid positions!")
            return False

        # Check if source has player's piece
        if not self.is_owned_by_current_player(from_x, from_y):
            print("That's not your piece!")
            return False

        # Check if destination is orthogonally adjacent
        if not ((abs(from_x - to_x) == 1 and from_y == to_y) or (abs(from_y - to_y) == 1 and from_x == to_x)):
            print("Pieces can only move orthogonally one space!")
            return False

        # Check if destination is empty or center (special case for Â)
        piece = self.board[from_x][from_y]
        target_piece = self.board[to_x][to_y]

        if target_piece != '_' and target_piece != '_':
            print("Destination is not empty!")
            return False

        # Special case for center (only Â can be there)
        if self.is_center(to_x, to_y) and piece != 'Â':
            print("Only Â can occupy the center!")
            return False

        # Perform the move
        self.board[from_x][from_y] = '_'
        self.board[to_x][to_y] = piece

        # Check for captures after move
        self.check_captures(to_x, to_y)

        # Check win conditions
        self.check_win_conditions()

        # Switch player if game isn't over
        if not self.game_over:
            self.current_player = 3 - self.current_player  # Switch between 1 and 2

        return True

    def check_captures(self, x, y):
        # Check all four orthogonal directions for captures
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        opponent = 'A' if self.current_player == 1 else 'V'
        
        for dx, dy in directions:
            nx1, ny1 = x + dx, y + dy
            nx2, ny2 = x - dx, y - dy
            
            # Check if both positions are valid
            if (self.is_valid_position(nx1, ny1) and self.is_valid_position(nx2, ny2)):
                piece1 = self.board[nx1][ny1]
                piece2 = self.board[nx2][ny2]
                
                # Check if sandwiched
                if (piece1 == opponent and piece2 == opponent):
                    captured_piece = self.board[x][y]
                    if captured_piece in ['V', 'A', 'Â']:
                        print(f"Captured {captured_piece} at ({x}, {y})!")
                        self.board[x][y] = '_'
                        return

    def check_win_conditions(self):
        # Check if Â is captured (Player 1 wins)
        â_pos = None
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 'Â':
                    â_pos = (i, j)
                    break
            if â_pos:
                break
        
        if not â_pos:
            self.game_over = True
            self.winner = 1
            print("Player 1 wins by capturing Â!")
            return

        # Check if Â reached border (Player 2 wins)
        if self.is_border(â_pos[0], â_pos[1]):
            self.game_over = True
            self.winner = 2
            print("Player 2 wins by moving Â to the border!")
            return

    def play(self):
        print("Welcome to Lilac!")
        print("Player 1 (V) vs Player 2 (A and Â)")
        print("Player 1 wins by capturing Â. Player 2 wins by moving Â to the border.")
        
        while not self.game_over:
            self.print_board()
            player_pieces = "V's" if self.current_player == 1 else "A's and Â"
            print(f"Player {self.current_player}'s turn ({player_pieces})")
            
            try:
                from_x, from_y = map(int, input("Enter piece to move (row col, 0-6): ").split())
                to_x, to_y = map(int, input("Enter destination (row col, 0-6): ").split())
                
                if not self.move_piece(from_x, from_y, to_x, to_y):
                    print("Invalid move, try again.")
            except ValueError:
                print("Please enter two numbers separated by a space.")
        
        self.print_board()
        print(f"Game over! Player {self.winner} wins!")

# Start the game
if __name__ == "__main__":
    game = LilacGame()
    game.play()