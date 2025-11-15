class Lazuli:
    def __init__(self):
        # Initialize 7x7 board
        self.board = self._create_initial_board()
        self.game_over = False
        self.won = False
    
    def _create_initial_board(self):
        # Create an empty 7x7 board
        board = [[' ' for _ in range(7)] for _ in range(7)]
        
        # Mark null spaces (2x2 corners)
        null_positions = [(0, 0), (0, 1), (1, 0), (1, 1),  # Top-left corner
                          (0, 5), (0, 6), (1, 5), (1, 6),  # Top-right corner
                          (5, 0), (5, 1), (6, 0), (6, 1),  # Bottom-left corner
                          (5, 5), (5, 6), (6, 5), (6, 6)]  # Bottom-right corner
        
        # Fill the board with 'X' pieces except for null spaces and center
        for row in range(7):
            for col in range(7):
                if (row, col) not in null_positions:
                    board[row][col] = 'X'
        
        # Center is empty
        board[3][3] = ' '
        
        return board
    
    def display_board(self):
        """Display the current board state"""
        print("  0 1 2 3 4 5 6")
        print(" +-+-+-+-+-+-+-+")
        for i, row in enumerate(self.board):
            print(f"{i}|", end="")
            for cell in row:
                print(f"{cell}|", end="")
            print("\n +-+-+-+-+-+-+-+")
    
    def get_valid_moves(self):
        """Return a list of valid moves in the format [(from_row, from_col, to_row, to_col), ...]"""
        valid_moves = []
        
        for row in range(7):
            for col in range(7):
                if self.board[row][col] == 'X':
                    # Check for jumps in all four directions
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
                    
                    for dr, dc in directions:
                        # Position of the piece to jump over
                        jump_row, jump_col = row + dr, col + dc
                        # Landing position
                        landing_row, landing_col = row + 2*dr, col + 2*dc
                        
                        # Check if jump is valid
                        if (0 <= jump_row < 7 and 0 <= jump_col < 7 and
                            0 <= landing_row < 7 and 0 <= landing_col < 7 and
                            self.board[jump_row][jump_col] == 'X' and
                            self.board[landing_row][landing_col] == ' '):
                            valid_moves.append((row, col, landing_row, landing_col))
        
        return valid_moves
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Make a move from (from_row, from_col) to (to_row, to_col)"""
        # Calculate the position of the jumped piece
        jumped_row = (from_row + to_row) // 2
        jumped_col = (from_col + to_col) // 2
        
        # Move the piece
        self.board[from_row][from_col] = ' '
        self.board[jumped_row][jumped_col] = ' '  # Remove the jumped piece
        self.board[to_row][to_col] = 'X'
        
        # Check if the game is over after this move
        self._check_game_over()
        
        return True
    
    def _check_game_over(self):
        """Check if the game is over and update game state accordingly"""
        # Count remaining pieces
        piece_count = sum(row.count('X') for row in self.board)
        
        # Check win condition: only one piece left at the center
        if piece_count == 1 and self.board[3][3] == 'X':
            self.game_over = True
            self.won = True
            return
        
        # Check if there are no valid moves left
        if not self.get_valid_moves():
            self.game_over = True
            self.won = False
            return
    
    def play(self):
        """Main game loop for interactive play"""
        print("Welcome to Lazuli!")
        print("The goal is to have only one piece left, and it must be in the center.")
        
        while not self.game_over:
            self.display_board()
            valid_moves = self.get_valid_moves()
            
            if not valid_moves:
                print("No more valid moves. You lose!")
                break
            
            print(f"You have {len(valid_moves)} valid moves.")
            
            # Display available moves
            for i, (fr, fc, tr, tc) in enumerate(valid_moves):
                print(f"{i+1}. Move from ({fr},{fc}) to ({tr},{tc})")
            
            # Get player choice
            try:
                choice = int(input("Enter move number: ")) - 1
                if 0 <= choice < len(valid_moves):
                    from_row, from_col, to_row, to_col = valid_moves[choice]
                    self.make_move(from_row, from_col, to_row, to_col)
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Display final board
        self.display_board()
        
        if self.won:
            print("Congratulations! You won!")
        else:
            print("Game over. You lost!")


if __name__ == "__main__":
    game = Lazuli()
    game.play()