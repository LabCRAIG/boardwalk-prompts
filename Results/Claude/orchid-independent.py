import numpy as np

class Orchid:
    def __init__(self):
        # Initialize 5x5 board with empty spaces
        self.board = np.full((5, 5), ' ')
        
        # Piece counts for each player
        self.player1_pieces = 12  # A's
        self.player2_pieces = 12  # B's
        
        # Pieces in hand (not yet placed)
        self.player1_hand = 12
        self.player2_hand = 12
        
        # Current game phase (1 = placement, 2 = movement)
        self.phase = 1
        
        # Current player (1 or 2)
        self.current_player = 1
        
        # Middle position is (2, 2)
        self.middle = (2, 2)
    
    def print_board(self):
        """Print the current state of the board"""
        # Print column numbers
        print('   ', end='')
        for col in range(5):
            print(f" {col} ", end='')
        print('\n   ' + '+--' * 5 + '+')
        
        # Print rows with row numbers
        for row in range(5):
            print(f' {row} |', end='')
            for col in range(5):
                print(f" {self.board[row, col]} |", end='')
            print('\n   ' + '+--' * 5 + '+')
    
    def place_piece(self, row, col):
        """Place a piece on the board during phase 1"""
        # Check if position is valid
        if not (0 <= row < 5 and 0 <= col < 5):
            print("Position out of bounds!")
            return False
        
        # Check if position is the middle
        if (row, col) == self.middle:
            print("Cannot place a piece in the middle!")
            return False
        
        # Check if position is already occupied
        if self.board[row, col] != ' ':
            print("Position already occupied!")
            return False
        
        # Place the piece
        piece = 'A' if self.current_player == 1 else 'B'
        self.board[row, col] = piece
        
        # Decrement pieces in hand
        if self.current_player == 1:
            self.player1_hand -= 1
        else:
            self.player2_hand -= 1
        
        return True
    
    def get_valid_moves(self, row, col):
        """Get all valid orthogonal moves for a piece"""
        if self.board[row, col] != ('A' if self.current_player == 1 else 'B'):
            return []
        
        valid_moves = []
        
        # Check in all 4 orthogonal directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                # Check if position is on board
                if not (0 <= r < 5 and 0 <= c < 5):
                    break
                # Check if position is free
                if self.board[r, c] == ' ':
                    valid_moves.append((r, c))
                else:
                    break
        
        return valid_moves
    
    def move_piece(self, from_pos, to_pos):
        """Move a piece and handle captures"""
        row, col = from_pos
        new_row, new_col = to_pos
        
        # Check if move is valid
        if (new_row, new_col) not in self.get_valid_moves(row, col):
            print("Invalid move!")
            return False
        
        # Move the piece
        piece = self.board[row, col]
        self.board[row, col] = ' '
        self.board[new_row, new_col] = piece
        
        # Check for captures in all orthogonal directions
        self.check_captures(new_row, new_col)
        
        return True
    
    def check_captures(self, row, col):
        """Check and handle captures after a move"""
        current_piece = 'A' if self.current_player == 1 else 'B'
        opponent_piece = 'B' if self.current_player == 1 else 'A'
        
        # Check in all 4 orthogonal directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for dr, dc in directions:
            # Check if there's an opponent's piece in this direction
            captured_positions = []
            r, c = row, col
            
            # Move in the direction to find opponent pieces
            while True:
                r += dr
                c += dc
                
                # If out of bounds or empty space, break
                if not (0 <= r < 5 and 0 <= c < 5) or self.board[r, c] == ' ':
                    break
                
                # If we find our own piece after opponent pieces, we have a capture
                if self.board[r, c] == current_piece and captured_positions:
                    # Capture all opponent pieces between
                    for capture_row, capture_col in captured_positions:
                        self.board[capture_row, capture_col] = ' '
                        if self.current_player == 1:
                            self.player2_pieces -= 1
                        else:
                            self.player1_pieces -= 1
                    break
                
                # If we find opponent's piece, add to potential captures
                if self.board[r, c] == opponent_piece:
                    captured_positions.append((r, c))
    
    def has_valid_moves(self):
        """Check if current player has any valid moves in phase 2"""
        piece = 'A' if self.current_player == 1 else 'B'
        
        # Check all positions
        for row in range(5):
            for col in range(5):
                if self.board[row, col] == piece and self.get_valid_moves(row, col):
                    return True
        
        return False
    
    def switch_player(self):
        """Switch to other player"""
        self.current_player = 3 - self.current_player  # 1->2, 2->1
    
    def play(self):
        """Main game loop"""
        game_over = False
        
        while not game_over:
            self.print_board()
            player_name = "Player 1 (A)" if self.current_player == 1 else "Player 2 (B)"
            
            if self.phase == 1:
                print(f"\n{player_name}'s turn (Placement Phase)")
                print(f"Pieces left to place: {self.player1_hand if self.current_player == 1 else self.player2_hand}")
                
                # Place two pieces
                for i in range(2):
                    if (self.current_player == 1 and self.player1_hand > 0) or \
                       (self.current_player == 2 and self.player2_hand > 0):
                        placed = False
                        while not placed:
                            try:
                                row = int(input(f"Enter row for piece {i+1}: "))
                                col = int(input(f"Enter column for piece {i+1}: "))
                                placed = self.place_piece(row, col)
                            except ValueError:
                                print("Please enter valid numbers for row and column.")
                
                # Check if placement phase is over
                if self.player1_hand == 0 and self.player2_hand == 0:
                    print("\nAll pieces placed! Moving to movement phase.")
                    self.phase = 2
            
            else:  # Phase 2 (movement)
                print(f"\n{player_name}'s turn (Movement Phase)")
                print(f"Player 1 (A) has {self.player1_pieces} pieces")
                print(f"Player 2 (B) has {self.player2_pieces} pieces")
                
                # Check for game over
                if self.player1_pieces == 0:
                    print("Player 2 (B) wins by capturing all opponent pieces!")
                    game_over = True
                    continue
                elif self.player2_pieces == 0:
                    print("Player 1 (A) wins by capturing all opponent pieces!")
                    game_over = True
                    continue
                
                # Check if player has valid moves
                if not self.has_valid_moves():
                    print(f"{player_name} has no valid moves and passes.")
                    self.switch_player()
                    continue
                
                # Select piece to move
                valid_selection = False
                while not valid_selection:
                    try:
                        row = int(input("Select piece row: "))
                        col = int(input("Select piece column: "))
                        
                        if not (0 <= row < 5 and 0 <= col < 5):
                            print("Position out of bounds!")
                            continue
                        
                        piece = 'A' if self.current_player == 1 else 'B'
                        if self.board[row, col] != piece:
                            print("You must select your own piece!")
                            continue
                        
                        valid_moves = self.get_valid_moves(row, col)
                        if not valid_moves:
                            print("This piece has no valid moves. Choose another piece.")
                            continue
                        
                        valid_selection = True
                    except ValueError:
                        print("Please enter valid numbers for row and column.")
                
                # Display valid moves
                print("Valid moves:")
                for i, (move_row, move_col) in enumerate(valid_moves):
                    print(f"{i+1}: ({move_row}, {move_col})")
                
                # Select destination
                valid_move = False
                while not valid_move:
                    try:
                        move_idx = int(input("Select move number: ")) - 1
                        if 0 <= move_idx < len(valid_moves):
                            destination = valid_moves[move_idx]
                            valid_move = self.move_piece((row, col), destination)
                        else:
                            print("Invalid move selection!")
                    except ValueError:
                        print("Please enter a valid move number.")
            
            # Switch to next player
            self.switch_player()
        
        # Final board state
        print("\nFinal board state:")
        self.print_board()


if __name__ == "__main__":
    print("Welcome to Orchid!")
    print("Player 1 controls A pieces, Player 2 controls B pieces")
    print("Phase 1: Each player places two pieces per turn")
    print("Phase 2: Move pieces orthogonally to capture opponent pieces")
    print("Win by capturing all opponent pieces")
    
    game = Orchid()
    game.play()
