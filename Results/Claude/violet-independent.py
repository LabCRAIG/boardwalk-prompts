import numpy as np

class Violet:
    def __init__(self):
        # Initialize 10x10 board with empty spaces
        self.board = np.full((10, 10), ' ')
        
        # Place initial pieces
        # Player 1 (A) pieces
        self.board[6, 0] = 'A'
        self.board[6, 9] = 'A'
        self.board[9, 3] = 'A'
        self.board[9, 6] = 'A'
        
        # Player 2 (V) pieces
        self.board[0, 3] = 'V'
        self.board[0, 6] = 'V'
        self.board[3, 0] = 'V'
        self.board[3, 9] = 'V'
        
        # Initialize current player (1 starts)
        self.current_player = 1
        
    def print_board(self):
        """Print the current state of the board"""
        # Print column numbers
        print('   ', end='')
        for col in range(10):
            print(f" {col} ", end='')
        print('\n   ' + '+--' * 10 + '+')
        
        # Print rows with row numbers
        for row in range(10):
            print(f' {row} |', end='')
            for col in range(10):
                print(f" {self.board[row, col]} |", end='')
            print('\n   ' + '+--' * 10 + '+')
    
    def get_player_pieces(self):
        """Return positions of current player's pieces"""
        piece = 'A' if self.current_player == 1 else 'V'
        positions = []
        for row in range(10):
            for col in range(10):
                if self.board[row, col] == piece:
                    positions.append((row, col))
        return positions
    
    def get_valid_moves(self, row, col):
        """Get all valid moves for piece at (row, col)"""
        if self.board[row, col] not in ['A', 'V']:
            return []
        
        valid_moves = []
        # Check all 8 directions: horizontal, vertical, and diagonal
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), 
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                # Check if position is on board
                if not (0 <= r < 10 and 0 <= c < 10):
                    break
                # Check if position is free
                if self.board[r, c] == ' ':
                    valid_moves.append((r, c))
                else:
                    break
        
        return valid_moves
    
    def get_valid_shots(self, row, col):
        """Get all valid shot positions for piece at (row, col)"""
        # Same logic as valid moves
        return self.get_valid_moves(row, col)
    
    def move_piece(self, from_pos, to_pos):
        """Move piece from one position to another"""
        row, col = from_pos
        new_row, new_col = to_pos
        
        # Move the piece
        self.board[new_row, new_col] = self.board[row, col]
        self.board[row, col] = ' '
        
        return True
    
    def shoot_x(self, shooter_pos, target_pos):
        """Shoot an X from the shooter position to target position"""
        row, col = target_pos
        self.board[row, col] = 'X'
        return True
    
    def has_valid_moves(self):
        """Check if current player has any valid moves"""
        piece_positions = self.get_player_pieces()
        
        for pos in piece_positions:
            if self.get_valid_moves(*pos):
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
            player_name = "Player 1 (A)" if self.current_player == 1 else "Player 2 (V)"
            print(f"\n{player_name}'s turn")
            
            if not self.has_valid_moves():
                print(f"{player_name} has no valid moves and loses!")
                winner = "Player 2 (V)" if self.current_player == 1 else "Player 1 (A)"
                print(f"{winner} wins!")
                game_over = True
                continue
            
            # Get player's pieces
            pieces = self.get_player_pieces()
            print("Your pieces are at:")
            for i, (row, col) in enumerate(pieces):
                print(f"{i+1}: Position ({row}, {col})")
            
            # Select piece to move
            valid_selection = False
            while not valid_selection:
                try:
                    selection = int(input("Select a piece to move (enter the number): ")) - 1
                    if 0 <= selection < len(pieces):
                        selected_pos = pieces[selection]
                        valid_moves = self.get_valid_moves(*selected_pos)
                        if valid_moves:
                            valid_selection = True
                        else:
                            print("This piece has no valid moves. Choose another piece.")
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Display valid moves
            print("Valid moves:")
            for i, (row, col) in enumerate(valid_moves):
                print(f"{i+1}: Position ({row}, {col})")
            
            # Select destination
            valid_move = False
            while not valid_move:
                try:
                    move_selection = int(input("Select a destination (enter the number): ")) - 1
                    if 0 <= move_selection < len(valid_moves):
                        destination = valid_moves[move_selection]
                        self.move_piece(selected_pos, destination)
                        valid_move = True
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # After moving, get valid shots
            valid_shots = self.get_valid_shots(*destination)
            
            # Display valid shots
            print("Valid shots for X:")
            for i, (row, col) in enumerate(valid_shots):
                print(f"{i+1}: Position ({row}, {col})")
            
            # Select shot
            valid_shot = False
            while not valid_shot:
                try:
                    shot_selection = int(input("Select where to place X (enter the number): ")) - 1
                    if 0 <= shot_selection < len(valid_shots):
                        shot_pos = valid_shots[shot_selection]
                        self.shoot_x(destination, shot_pos)
                        valid_shot = True
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Switch to next player
            self.switch_player()
        
        # Final board state
        print("\nFinal board state:")
        self.print_board()


if __name__ == "__main__":
    print("Welcome to Violet!")
    print("Player 1 controls A pieces, Player 2 controls V pieces")
    print("On your turn, move one of your pieces and then shoot an X")
    print("Win by blocking your opponent so they can't move")
    
    game = Violet()
    game.play()
