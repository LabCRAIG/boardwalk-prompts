import numpy as np

class Topaz:
    def __init__(self):
        # Create a 7x7 board
        # 0 represents empty spaces, None represents null spaces
        # 1 for player 1 (A), 2 for player 2 (B)
        self.board = np.zeros((7, 7), dtype=object)
        self.board.fill(0)  # Fill with blank spaces initially
        
        # Set null spaces based on the initial setup (whitespaces)
        # We'll define the initial layout based on the game description
        # This is just an example - update based on actual layout needed
        
        # Players' remaining pieces
        self.player1_pieces = 9  # A pieces
        self.player2_pieces = 9  # B pieces
        
        # Pieces on the board
        self.player1_on_board = 0
        self.player2_on_board = 0
        
        # Current player (1 starts)
        self.current_player = 1
        
        # Game phase (1 = placement, 2 = movement)
        self.phase = 1
        
        # Game over flag
        self.game_over = False
        
        # Winner (0 = no winner yet, 1 or 2 = player who won)
        self.winner = 0
    
    def is_valid_position(self, row, col):
        """Check if a position is valid on the board."""
        return (0 <= row < 7 and 0 <= col < 7 and self.board[row, col] is not None)
    
    def is_position_empty(self, row, col):
        """Check if a position is empty (not null and not occupied)."""
        return self.is_valid_position(row, col) and self.board[row, col] == 0
    
    def are_adjacent(self, row1, col1, row2, col2):
        """Check if two positions are adjacent (closest blank spaces in same row/column)."""
        if row1 == row2:  # Same row
            # Check if they're the closest in the same row
            if col1 < col2:
                for c in range(col1 + 1, col2):
                    if self.is_valid_position(row1, c) and self.board[row1, c] == 0:
                        return False
                return True
            else:  # col1 > col2
                for c in range(col2 + 1, col1):
                    if self.is_valid_position(row1, c) and self.board[row1, c] == 0:
                        return False
                return True
        elif col1 == col2:  # Same column
            # Check if they're the closest in the same column
            if row1 < row2:
                for r in range(row1 + 1, row2):
                    if self.is_valid_position(r, col1) and self.board[r, col1] == 0:
                        return False
                return True
            else:  # row1 > row2
                for r in range(row2 + 1, row1):
                    if self.is_valid_position(r, col1) and self.board[r, col1] == 0:
                        return False
                return True
        return False  # Not in same row or column
    
    def check_capture(self, row, col):
        """Check if placing/moving a piece to (row, col) creates a capture condition."""
        player_symbol = self.current_player
        
        # Check horizontal line (row)
        count = 0
        for c in range(7):
            if self.is_valid_position(row, c) and self.board[row, c] == player_symbol:
                count += 1
                if count == 3:
                    return True
            else:
                count = 0
        
        # Check vertical line (column)
        count = 0
        for r in range(7):
            if self.is_valid_position(r, col) and self.board[r, col] == player_symbol:
                count += 1
                if count == 3:
                    return True
            else:
                count = 0
        
        return False
    
    def place_piece(self, row, col):
        """Place a piece during the placement phase."""
        if self.phase != 1:
            print("Not in placement phase!")
            return False
        
        if not self.is_position_empty(row, col):
            print("Position is not empty!")
            return False
        
        # Place the piece
        self.board[row, col] = self.current_player
        
        # Update piece counts
        if self.current_player == 1:
            self.player1_pieces -= 1
            self.player1_on_board += 1
        else:
            self.player2_pieces -= 1
            self.player2_on_board += 1
        
        # Check for capture
        captured = self.check_capture(row, col)
        
        # Switch to next player if no capture
        if not captured:
            self.current_player = 3 - self.current_player  # Switch between 1 and 2
        
        # Check if all pieces have been placed to move to phase 2
        if self.player1_pieces == 0 and self.player2_pieces == 0:
            self.phase = 2
            print("Moving to movement phase!")
        
        return captured
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move a piece during the movement phase."""
        if self.phase != 2:
            print("Not in movement phase!")
            return False
        
        # Check if 'from' position has current player's piece
        if not self.is_valid_position(from_row, from_col) or self.board[from_row, from_col] != self.current_player:
            print("Invalid 'from' position!")
            return False
        
        # Check if 'to' position is empty
        if not self.is_position_empty(to_row, to_col):
            print("'To' position is not empty!")
            return False
        
        # Check if positions are adjacent
        if not self.are_adjacent(from_row, from_col, to_row, to_col):
            print("Positions are not adjacent!")
            return False
        
        # Move the piece
        self.board[to_row, to_col] = self.current_player
        self.board[from_row, from_col] = 0
        
        # Check for capture
        captured = self.check_capture(to_row, to_col)
        
        # Switch to next player if no capture
        if not captured:
            self.current_player = 3 - self.current_player  # Switch between 1 and 2
            self.check_win_conditions()
        
        return captured
    
    def capture_piece(self, row, col):
        """Capture an opponent's piece."""
        opponent = 3 - self.current_player  # Get opponent's number
        
        if not self.is_valid_position(row, col) or self.board[row, col] != opponent:
            print("Invalid capture position!")
            return False
        
        # Remove the piece
        self.board[row, col] = 0
        
        # Update piece count
        if opponent == 1:
            self.player1_on_board -= 1
        else:
            self.player2_on_board -= 1
        
        # Check win conditions after capture
        self.check_win_conditions()
        
        # Switch to next player
        self.current_player = 3 - self.current_player
        
        return True
    
    def check_win_conditions(self):
        """Check if the game is over based on win/loss conditions."""
        if self.phase != 2:
            return  # Only check win conditions in phase 2
        
        # Check if a player has only 2 pieces left
        if self.player1_on_board <= 2:
            self.game_over = True
            self.winner = 2
            print("Player 2 wins! Player 1 has only 2 pieces left.")
            return
        
        if self.player2_on_board <= 2:
            self.game_over = True
            self.winner = 1
            print("Player 1 wins! Player 2 has only 2 pieces left.")
            return
        
        # Check if current player can't move any pieces
        if not self.can_player_move(self.current_player):
            self.game_over = True
            self.winner = 3 - self.current_player
            print(f"Player {3 - self.current_player} wins! Player {self.current_player} can't move any pieces.")
    
    def can_player_move(self, player):
        """Check if a player can move any of their pieces."""
        for r in range(7):
            for c in range(7):
                if self.is_valid_position(r, c) and self.board[r, c] == player:
                    # Check all four directions
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
                    for dr, dc in directions:
                        # Check if there's a valid adjacent space in this direction
                        row, col = r, c
                        while True:
                            row += dr
                            col += dc
                            if not self.is_valid_position(row, col):
                                break
                            if self.board[row, col] == 0:  # Empty space found
                                return True
                            elif self.board[row, col] is not None:  # Piece found
                                break
        return False
    
    def display_board(self):
        """Display the current board state."""
        symbols = {0: '_', 1: 'A', 2: 'B', None: ' '}
        print("  0 1 2 3 4 5 6")
        for r in range(7):
            row_str = f"{r} "
            for c in range(7):
                row_str += symbols[self.board[r, c]] + " "
            print(row_str)
        print()
    
    def play_game(self):
        """Interactive game play."""
        print("Welcome to Topaz!")
        print("Player 1: A, Player 2: B")
        
        while not self.game_over:
            self.display_board()
            print(f"Player {self.current_player}'s turn")
            
            if self.phase == 1:
                print(f"Phase: Placement (Player 1 has {self.player1_pieces} pieces left, Player 2 has {self.player2_pieces} pieces left)")
                valid_input = False
                while not valid_input:
                    try:
                        row = int(input("Enter row to place piece: "))
                        col = int(input("Enter column to place piece: "))
                        
                        captured = self.place_piece(row, col)
                        if captured:
                            print("Capture condition met! You can remove an opponent's piece.")
                            valid_removal = False
                            while not valid_removal:
                                try:
                                    r = int(input("Enter row of piece to remove: "))
                                    c = int(input("Enter column of piece to remove: "))
                                    valid_removal = self.capture_piece(r, c)
                                except ValueError:
                                    print("Invalid input. Please enter integers.")
                        valid_input = True
                    except ValueError:
                        print("Invalid input. Please enter integers.")
            
            else:  # Phase 2
                print("Phase: Movement")
                valid_input = False
                while not valid_input:
                    try:
                        from_row = int(input("Enter row of piece to move: "))
                        from_col = int(input("Enter column of piece to move: "))
                        to_row = int(input("Enter row to move to: "))
                        to_col = int(input("Enter column to move to: "))
                        
                        captured = self.move_piece(from_row, from_col, to_row, to_col)
                        if captured:
                            print("Capture condition met! You can remove an opponent's piece.")
                            valid_removal = False
                            while not valid_removal:
                                try:
                                    r = int(input("Enter row of piece to remove: "))
                                    c = int(input("Enter column of piece to remove: "))
                                    valid_removal = self.capture_piece(r, c)
                                except ValueError:
                                    print("Invalid input. Please enter integers.")
                        valid_input = True
                    except ValueError:
                        print("Invalid input. Please enter integers.")
            
            if self.game_over:
                self.display_board()
                print(f"Game over! Player {self.winner} wins!")

# Main execution
if __name__ == "__main__":
    game = Topaz()
    
    # Initialize the board with null spaces if needed
    # This is where you would set the null spaces based on the game's initial setup
    # For example:
    # game.board[0, 0] = None
    
    game.play_game()