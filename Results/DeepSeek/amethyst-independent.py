class AmethystGame:
    def __init__(self):
        self.board_size = 8
        self.reset_game()
        
    def reset_game(self):
        # Initialize the board according to the setup
        self.board = [
            [' ', 'O', ' ', 'O', ' ', 'O', ' ', 'O'],
            ['O', ' ', 'O', ' ', 'O', ' ', 'O', ' '],
            [' ', 'O', ' ', 'O', ' ', 'O', ' ', 'O'],
            ['_', ' ', '_', ' ', '_', ' ', '_', ' '],
            [' ', '_', ' ', '_', ' ', '_', ' ', '_'],
            ['A', ' ', 'A', ' ', 'A', ' ', 'A', ' '],
            [' ', 'A', ' ', 'A', ' ', 'A', ' ', 'A'],
            ['A', ' ', 'A', ' ', 'A', ' ', 'A', ' ']
        ]
        self.current_player = 1  # Player 1 starts
        self.game_over = False
        self.winner = None
        self.last_capture_pos = None  # Track position of piece that made a capture
        
    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i, row in enumerate(self.board):
            print(i, end=" ")
            for cell in row:
                print(cell, end=" ")
            print()
        print()
        
    def is_valid_position(self, row, col):
        return 0 <= row < self.board_size and 0 <= col < self.board_size
        
    def get_piece_direction(self, piece):
        if piece == 'A':
            return -1  # Only moves upward (decreasing row)
        elif piece == 'O':
            return 1   # Only moves downward (increasing row)
        elif piece in ('Â', 'Ô'):
            return 0  # Can move both directions
        return None
        
    def is_own_piece(self, piece):
        if self.current_player == 1:
            return piece in ('A', 'Â')
        else:
            return piece in ('O', 'Ô')
            
    def can_promote(self, row, col):
        piece = self.board[row][col]
        if piece == 'A' and row == 0:
            return True
        if piece == 'O' and row == self.board_size - 1:
            return True
        return False
        
    def promote_piece(self, row, col):
        piece = self.board[row][col]
        if piece == 'A':
            self.board[row][col] = 'Â'
        elif piece == 'O':
            self.board[row][col] = 'Ô'
            
    def get_valid_moves(self, row, col, must_capture=False):
        moves = []
        piece = self.board[row][col]
        if piece == ' ' or piece == '_':
            return moves
            
        # Check if we're forced to capture with this piece
        if must_capture and (row, col) != self.last_capture_pos:
            return moves
            
        # Determine allowed move directions
        directions = []
        piece_dir = self.get_piece_direction(piece)
        if piece_dir == -1:  # A (up only)
            directions.append((-1, -1))
            directions.append((-1, 1))
        elif piece_dir == 1:  # O (down only)
            directions.append((1, -1))
            directions.append((1, 1))
        else:  # Â or Ô (both directions)
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
            
        # Check for regular moves and captures
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                if self.board[new_row][new_col] == '_':
                    if not must_capture:
                        moves.append((new_row, new_col, False))
                elif not self.is_own_piece(self.board[new_row][new_col]):
                    # Check if we can capture
                    jump_row, jump_col = new_row + dr, new_col + dc
                    if self.is_valid_position(jump_row, jump_col) and \
                       self.board[jump_row][jump_col] == '_':
                        moves.append((jump_row, jump_col, True))
                        
        return moves
        
    def has_any_valid_move(self, player):
        # Check if player has any valid moves (including captures)
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                if (player == 1 and piece in ('A', 'Â')) or (player == 2 and piece in ('O', 'Ô')):
                    if self.get_valid_moves(row, col) or self.get_valid_moves(row, col, must_capture=True):
                        return True
        return False
        
    def count_pieces(self, player):
        count = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                if (player == 1 and piece in ('A', 'Â')) or (player == 2 and piece in ('O', 'Ô')):
                    count += 1
        return count
        
    def move_piece(self, start_row, start_col, end_row, end_col):
        # Validate move
        if not self.is_valid_position(start_row, start_col) or not self.is_valid_position(end_row, end_col):
            return False, "Invalid positions"
            
        piece = self.board[start_row][start_col]
        if piece == ' ' or piece == '_':
            return False, "No piece at starting position"
            
        if not self.is_own_piece(piece):
            return False, "That's not your piece"
            
        # Check if we must capture
        must_capture = self.last_capture_pos is not None
        valid_moves = self.get_valid_moves(start_row, start_col, must_capture)
        
        # Find the specific move we're trying to make
        move_made = None
        for move in valid_moves:
            if move[0] == end_row and move[1] == end_col:
                move_made = move
                break
                
        if not move_made:
            return False, "Invalid move"
            
        is_capture = move_made[2]
        
        # Make the move
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = '_'
        
        # Handle captures
        if is_capture:
            # Remove the captured piece
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            self.board[mid_row][mid_col] = '_'
            self.last_capture_pos = (end_row, end_col)
            
            # Check for additional captures with the same piece
            additional_captures = self.get_valid_moves(end_row, end_col, must_capture=True)
            if additional_captures:
                # Player must continue capturing
                return True, "Continue capturing with this piece"
        
        # Check for promotion
        if self.can_promote(end_row, end_col):
            self.promote_piece(end_row, end_col)
            
        # Reset capture tracking if no more captures
        if not is_capture or not self.get_valid_moves(end_row, end_col, must_capture=True):
            self.last_capture_pos = None
            self.current_player = 3 - self.current_player  # Switch player
            
        # Check win conditions
        opponent = 3 - self.current_player
        if self.count_pieces(opponent) == 0 or not self.has_any_valid_move(opponent):
            self.game_over = True
            self.winner = self.current_player
            return True, f"Player {self.current_player} wins!"
            
        return True, "Move successful"
        
    def play(self):
        print("Welcome to Amethyst!")
        print("Player 1: A/Â (moves upward)")
        print("Player 2: O/Ô (moves downward)")
        print("Enter moves as 'start_row start_col end_row end_col'")
        print()
        
        while not self.game_over:
            self.print_board()
            print(f"Player {self.current_player}'s turn")
            
            # Check if player has valid moves
            if not self.has_any_valid_move(self.current_player):
                self.game_over = True
                self.winner = 3 - self.current_player
                print(f"Player {self.current_player} has no valid moves!")
                break
                
            # Get move input
            while True:
                try:
                    move = input("Enter your move: ").strip()
                    if move.lower() == 'exit':
                        print("Game ended by user.")
                        return
                        
                    parts = list(map(int, move.split()))
                    if len(parts) != 4:
                        raise ValueError
                        
                    start_row, start_col, end_row, end_col = parts
                    success, message = self.move_piece(start_row, start_col, end_row, end_col)
                    print(message)
                    if success:
                        break
                except ValueError:
                    print("Invalid input. Please enter 4 numbers separated by spaces.")
                    
        if self.winner:
            print(f"Player {self.winner} wins!")
        else:
            print("Game ended in a draw.")
            
        print("Final board:")
        self.print_board()


# Start the game
if __name__ == "__main__":
    game = AmethystGame()
    game.play()