import numpy as np

class DaisyGame:
    def __init__(self):
        # Initialize 9x9 board with empty spaces
        self.board = np.full((9, 9), ' ')
        
        # Initialize player reserves
        self.p1_reserve = {'A': 1, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2, 'G': 2, 'H': 9}
        self.p2_reserve = {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'e': 2, 'f': 2, 'g': 2, 'h': 9}
        
        # Track if kings are on board
        self.p1_king_placed = False
        self.p2_king_placed = False
        
        # Current player (1 or 2)
        self.current_player = 1
        
        # Game status
        self.game_over = False
        self.winner = None
    
    def print_board(self):
        """Print the current state of the board"""
        # Print column numbers
        print('\n    ', end='')
        for col in range(9):
            print(f" {col} ", end='')
        print('\n    ' + '+--' * 9 + '+')
        
        # Print rows with row numbers
        for row in range(9):
            print(f' {row}  |', end='')
            for col in range(9):
                print(f" {self.board[row, col]} |", end='')
            print()
            print('    ' + '+--' * 9 + '+')
    
    def print_reserves(self):
        """Print the current state of player reserves"""
        print("\nPlayer 1 Reserve:")
        for piece, count in self.p1_reserve.items():
            if count > 0:
                print(f"{piece}: {count}", end="  ")
        
        print("\nPlayer 2 Reserve:")
        for piece, count in self.p2_reserve.items():
            if count > 0:
                print(f"{piece}: {count}", end="  ")
        print("\n")
    
    def place_piece(self, piece, row, col):
        """Place a piece from reserve onto the board"""
        # Validate piece belongs to current player
        if self.current_player == 1 and piece not in self.p1_reserve:
            return False, "That piece doesn't belong to Player 1."
        elif self.current_player == 2 and piece not in self.p2_reserve:
            return False, "That piece doesn't belong to Player 2."
        
        # Check if piece is available in reserve
        if self.current_player == 1 and self.p1_reserve[piece] <= 0:
            return False, f"No {piece} pieces left in reserve."
        elif self.current_player == 2 and self.p2_reserve[piece] <= 0:
            return False, f"No {piece} pieces left in reserve."
        
        # Check if position is valid
        if not (0 <= row < 9 and 0 <= col < 9):
            return False, "Position out of bounds."
        
        # Check if position is empty
        if self.board[row, col] != ' ':
            return False, "Position already occupied."
        
        # Place the piece
        self.board[row, col] = piece
        
        # Update reserve
        if self.current_player == 1:
            self.p1_reserve[piece] -= 1
            if piece == 'A':
                self.p1_king_placed = True
        else:
            self.p2_reserve[piece] -= 1
            if piece == 'a':
                self.p2_king_placed = True
        
        return True, f"Placed {piece} at position ({row}, {col})."
    
    def get_valid_moves(self, row, col):
        """Get all valid moves for a piece at the given position"""
        piece = self.board[row, col]
        
        # Check if position is valid and contains a piece
        if not (0 <= row < 9 and 0 <= col < 9) or piece == ' ':
            return []
        
        # Check if piece belongs to current player
        if (self.current_player == 1 and piece.islower()) or (self.current_player == 2 and piece.isupper()):
            return []
        
        valid_moves = []
        # Determine piece type (normalize to uppercase for comparison)
        piece_type = piece.upper()
        
        # For player 1 (uppercase), forward is up (-1 in row)
        # For player 2 (lowercase), forward is down (+1 in row)
        forward_dir = -1 if piece.isupper() else 1
        
        # Handle movement based on piece type
        if piece_type == 'A':  # A, a: moves one space in any direction
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < 9 and 0 <= c < 9:
                    # Can move to empty space or capture
                    target = self.board[r, c]
                    if target == ' ' or (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                        valid_moves.append((r, c))
        
        elif piece_type == 'B':  # B, b: moves any number of spaces orthogonally
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dr, dc in directions:
                r, c = row, col
                while True:
                    r += dr
                    c += dc
                    if not (0 <= r < 9 and 0 <= c < 9):
                        break
                    target = self.board[r, c]
                    if target == ' ':
                        valid_moves.append((r, c))
                    elif (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                        valid_moves.append((r, c))
                        break
                    else:
                        break
        
        elif piece_type == 'C':  # C, c: moves any number of spaces diagonally
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                r, c = row, col
                while True:
                    r += dr
                    c += dc
                    if not (0 <= r < 9 and 0 <= c < 9):
                        break
                    target = self.board[r, c]
                    if target == ' ':
                        valid_moves.append((r, c))
                    elif (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                        valid_moves.append((r, c))
                        break
                    else:
                        break
        
        elif piece_type == 'D':  # D, d: moves one square in any direction except diagonally backwards
            # All directions except diagonally backward
            directions = [
                (forward_dir, 0),  # Forward
                (0, 1), (0, -1),    # Left and right
                (forward_dir, 1), (forward_dir, -1)  # Diagonally forward
            ]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < 9 and 0 <= c < 9:
                    target = self.board[r, c]
                    if target == ' ' or (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                        valid_moves.append((r, c))
        
        elif piece_type == 'E':  # E, e: moves one square diagonally or one square forward orthogonally
            # Diagonally in any direction or forward orthogonally
            directions = [
                (forward_dir, 0),  # Forward
                (1, 1), (1, -1), (-1, 1), (-1, -1)  # All diagonals
            ]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < 9 and 0 <= c < 9:
                    target = self.board[r, c]
                    if target == ' ' or (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                        valid_moves.append((r, c))
        
        elif piece_type == 'F':  # F, f: moves two spaces forward and then one space either left or right
            # Forward two then left or right one (like knight but only forward)
            r = row + (2 * forward_dir)
            if 0 <= r < 9:
                for c in [col - 1, col + 1]:
                    if 0 <= c < 9:
                        target = self.board[r, c]
                        if target == ' ' or (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                            valid_moves.append((r, c))
        
        elif piece_type == 'G':  # G, g: moves any number of spaces only orthogonally forward
            # Any number of spaces forward
            r, c = row, col
            while True:
                r += forward_dir
                if not (0 <= r < 9):
                    break
                target = self.board[r, c]
                if target == ' ':
                    valid_moves.append((r, c))
                elif (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                    valid_moves.append((r, c))
                    break
                else:
                    break
        
        elif piece_type == 'H':  # H, h: moves one space forward orthogonally
            # One space forward
            r = row + forward_dir
            c = col
            if 0 <= r < 9:
                target = self.board[r, c]
                if target == ' ' or (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                    valid_moves.append((r, c))
        
        return valid_moves
    
    def move_piece(self, from_pos, to_pos):
        """Move a piece from one position to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Get the piece
        piece = self.board[from_row, from_col]
        
        # Check if move is valid
        valid_moves = self.get_valid_moves(from_row, from_col)
        if (to_row, to_col) not in valid_moves:
            return False, "Invalid move for this piece."
        
        # Check if player can capture (kings must be on board)
        target = self.board[to_row, to_col]
        if target != ' ':  # This is a capture
            if (self.current_player == 1 and not self.p1_king_placed) or \
               (self.current_player == 2 and not self.p2_king_placed):
                return False, f"Cannot capture until your {'A' if self.current_player == 1 else 'a'} is on the board."
            
            # Handle capture
            if target == 'a' and self.current_player == 1:
                self.game_over = True
                self.winner = 1
            elif target == 'A' and self.current_player == 2:
                self.game_over = True
                self.winner = 2
            
            # Add captured piece to reserve (converting to the appropriate type)
            equivalent_piece = target.upper() if self.current_player == 1 else target.lower()
            if self.current_player == 1:
                self.p1_reserve[equivalent_piece] += 1
            else:
                self.p2_reserve[equivalent_piece] += 1
        
        # Move the piece
        self.board[to_row, to_col] = piece
        self.board[from_row, from_col] = ' '
        
        return True, f"Moved {piece} from ({from_row}, {from_col}) to ({to_row}, {to_col})."
    
    def switch_player(self):
        """Switch to other player"""
        self.current_player = 3 - self.current_player  # 1->2, 2->1
    
    def play(self):
        """Main game loop"""
        print("Welcome to Daisy!")
        print("Player 1 controls uppercase pieces (A-H)")
        print("Player 2 controls lowercase pieces (a-h)")
        print("Win by capturing your opponent's king (A or a)")
        
        while not self.game_over:
            self.print_board()
            self.print_reserves()
            
            player_name = "Player 1" if self.current_player == 1 else "Player 2"
            piece_set = "uppercase (A-H)" if self.current_player == 1 else "lowercase (a-h)"
            print(f"\n{player_name}'s turn (controlling {piece_set} pieces)")
            
            # Player selects action
            print("Select action:")
            print("1. Place a piece from reserve")
            print("2. Move a piece on the board")
            
            action = input("Enter choice (1 or 2): ").strip()
            
            if action == '1':  # Place a piece from reserve
                # Show available pieces
                available = self.p1_reserve if self.current_player == 1 else self.p2_reserve
                print("Available pieces in reserve:")
                for piece, count in available.items():
                    if count > 0:
                        print(f"{piece}: {count}", end="  ")
                print()
                
                # Select piece and position
                piece = input("Enter piece to place: ").strip()
                try:
                    row = int(input("Enter row: "))
                    col = int(input("Enter column: "))
                    success, message = self.place_piece(piece, row, col)
                    print(message)
                    if success:
                        self.switch_player()
                except ValueError:
                    print("Invalid input. Row and column must be numbers.")
            
            elif action == '2':  # Move a piece
                try:
                    from_row = int(input("Enter row of piece to move: "))
                    from_col = int(input("Enter column of piece to move: "))
                    
                    # Validate selection
                    if not (0 <= from_row < 9 and 0 <= from_col < 9):
                        print("Position out of bounds.")
                        continue
                    
                    piece = self.board[from_row, from_col]
                    if piece == ' ':
                        print("No piece at that position.")
                        continue
                    
                    if (self.current_player == 1 and piece.islower()) or \
                       (self.current_player == 2 and piece.isupper()):
                        print("That's not your piece.")
                        continue
                    
                    # Show valid moves
                    valid_moves = self.get_valid_moves(from_row, from_col)
                    if not valid_moves:
                        print("No valid moves for this piece.")
                        continue
                    
                    print("Valid moves:")
                    for i, (r, c) in enumerate(valid_moves):
                        target = " " if self.board[r, c] == ' ' else self.board[r, c]
                        print(f"{i+1}: ({r}, {c}) {target}")
                    
                    # Select move
                    move_idx = int(input("Select move number: ")) - 1
                    if 0 <= move_idx < len(valid_moves):
                        to_pos = valid_moves[move_idx]
                        success, message = self.move_piece((from_row, from_col), to_pos)
                        print(message)
                        if success:
                            self.switch_player()
                    else:
                        print("Invalid move selection.")
                
                except ValueError:
                    print("Invalid input. Please enter numbers.")
            
            else:
                print("Invalid action. Please enter 1 or 2.")
            
            # Check for game over
            if self.game_over:
                self.print_board()
                print(f"Player {self.winner} wins!")


if __name__ == "__main__":
    game = DaisyGame()
    game.play()
