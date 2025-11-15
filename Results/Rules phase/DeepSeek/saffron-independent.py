class SaffronGame:
    def __init__(self):
        self.board_size = 8
        self.board = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Initial piece placement (diagonally opposite center)
        center = self.board_size // 2
        self.board[center-1][center-1] = 'A'  # Player 1's piece
        self.board[center][center] = 'B'      # Player 2's piece
        
        # Track positions
        self.a_pos = (center-1, center-1)
        self.b_pos = (center, center)
        
        self.current_player = 1  # Player 1 starts
        self.game_over = False
        self.winner = None
        
    def print_board(self):
        print("  " + " ".join(str(i) for i in range(self.board_size)))
        for i, row in enumerate(self.board):
            print(i, " ".join(row))
        print()
    
    def is_valid_move(self, from_pos, to_pos):
        # Check if move is orthogonal (not diagonal)
        dx = abs(to_pos[0] - from_pos[0])
        dy = abs(to_pos[1] - from_pos[1])
        
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)
    
    def move_piece(self, to_row, to_col):
        if self.game_over:
            print("Game is already over!")
            return False
            
        if self.current_player == 1:
            piece = 'A'
            from_pos = self.a_pos
        else:
            piece = 'B'
            from_pos = self.b_pos
            
        # Check if target position is valid
        if not (0 <= to_row < self.board_size and 0 <= to_col < self.board_size):
            print("Move is outside the board!")
            return False
            
        # Check if moving to opponent's piece
        opponent_piece = 'B' if self.current_player == 1 else 'A'
        if self.board[to_row][to_col] == opponent_piece:
            print("Cannot move onto opponent's piece!")
            return False
            
        # Check if move is orthogonal
        if not self.is_valid_move(from_pos, (to_row, to_col)):
            print("Invalid move! Must move orthogonally (up, down, left, right).")
            return False
            
        # Check if moving to a marker (losing condition)
        if self.board[to_row][to_col] in ['a', 'b']:
            self.game_over = True
            self.winner = 2 if self.current_player == 1 else 1
            print(f"Player {self.current_player} moved onto a marker! Player {self.winner} wins!")
            return True
            
        # Place marker at current position
        marker = 'a' if self.current_player == 1 else 'b'
        self.board[from_pos[0]][from_pos[1]] = marker
        
        # Move the piece
        self.board[to_row][to_col] = piece
        if self.current_player == 1:
            self.a_pos = (to_row, to_col)
        else:
            self.b_pos = (to_row, to_col)
            
        # Switch players
        self.current_player = 2 if self.current_player == 1 else 1
        return True
    
    def play(self):
        print("Welcome to Saffron!")
        print("Player 1 controls A, Player 2 controls B")
        print("Move orthogonally (up, down, left, right)")
        print("Moving onto a marker (a or b) makes you lose!")
        print()
        
        while not self.game_over:
            self.print_board()
            player = self.current_player
            piece = 'A' if player == 1 else 'B'
            
            print(f"Player {player}'s turn ({piece})")
            try:
                row = int(input("Enter target row (0-7): "))
                col = int(input("Enter target column (0-7): "))
                self.move_piece(row, col)
            except ValueError:
                print("Please enter valid numbers!")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        self.print_board()
        print(f"Game over! Player {self.winner} wins!")

# To start the game:
if __name__ == "__main__":
    game = SaffronGame()
    game.play()