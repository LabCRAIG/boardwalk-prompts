import os
import time

class Lilac:
    def __init__(self):
        # Initialize the 7x7 board
        self.board = [['_' for _ in range(7)] for _ in range(7)]
        self.current_player = 1  # Player 1 starts (V's)
        self.game_over = False
        self.winner = None
        
        # Set up the initial board configuration
        # **VVV**
        # ***V***
        # V_AAA_V
        # VVAÂAVV
        # V_AAA_V
        # ***V***
        # **VVV**

        # Row 0
        self.board[0][2] = 'V'
        self.board[0][3] = 'V'
        self.board[0][4] = 'V'
        
        # Row 1
        self.board[1][3] = 'V'
        
        # Row 2
        self.board[2][0] = 'V'
        self.board[2][2] = 'A'
        self.board[2][3] = 'A'
        self.board[2][4] = 'A'
        self.board[2][6] = 'V'
        
        # Row 3 (middle row)
        self.board[3][0] = 'V'
        self.board[3][1] = 'V'
        self.board[3][2] = 'A'
        self.board[3][3] = 'Â'  # The special A piece
        self.board[3][4] = 'A'
        self.board[3][5] = 'V'
        self.board[3][6] = 'V'
        
        # Row 4
        self.board[4][0] = 'V'
        self.board[4][2] = 'A'
        self.board[4][3] = 'A'
        self.board[4][4] = 'A'
        self.board[4][6] = 'V'
        
        # Row 5
        self.board[5][3] = 'V'
        
        # Row 6
        self.board[6][2] = 'V'
        self.board[6][3] = 'V'
        self.board[6][4] = 'V'

    def display_board(self):
        """Display the current state of the board"""
        clear_screen()
        print(f"Player {self.current_player}'s turn")
        print("  0 1 2 3 4 5 6")
        for i, row in enumerate(self.board):
            print(f"{i} {' '.join(row)}")
        print()

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        """Check if a move is valid according to the game rules"""
        # Check if positions are on the board
        if not (0 <= from_row < 7 and 0 <= from_col < 7 and 0 <= to_row < 7 and 0 <= to_col < 7):
            return False
        
        # Check if the "from" position contains the current player's piece
        piece = self.board[from_row][from_col]
        if self.current_player == 1 and piece != 'V':
            return False
        if self.current_player == 2 and piece not in ['A', 'Â']:
            return False
        
        # Check if the "to" position is empty
        if self.board[to_row][to_col] != '_':
            return False
        
        # Check if move is orthogonal and only one space
        if (from_row == to_row and abs(from_col - to_col) == 1) or \
           (from_col == to_col and abs(from_row - to_row) == 1):
            # Check the center rule - only Â can occupy the center
            if to_row == 3 and to_col == 3 and piece != 'Â':
                return False
            return True
        
        return False

    def make_move(self, from_row, from_col, to_row, to_col):
        """Execute a move and update the board state"""
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False
        
        # Move the piece
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = '_'
        self.board[to_row][to_col] = piece
        
        # Check for captures after the move
        self.check_captures()
        
        # Check win conditions
        self.check_win_conditions()
        
        # Switch player
        if not self.game_over:
            self.current_player = 3 - self.current_player  # Alternates between 1 and 2
        
        return True

    def check_captures(self):
        """Check for sandwiched pieces and remove them"""
        pieces_to_remove = []
        
        # Check horizontally
        for row in range(7):
            for col in range(1, 6):  # Skip edges since they can't be sandwiched
                piece = self.board[row][col]
                if piece == '_':
                    continue
                
                left_piece = self.board[row][col-1]
                right_piece = self.board[row][col+1]
                
                # Check if the piece is sandwiched
                if piece in ['A', 'Â'] and left_piece == 'V' and right_piece == 'V':
                    pieces_to_remove.append((row, col))
                elif piece == 'V' and left_piece in ['A', 'Â'] and right_piece in ['A', 'Â']:
                    pieces_to_remove.append((row, col))
        
        # Check vertically
        for col in range(7):
            for row in range(1, 6):  # Skip edges
                piece = self.board[row][col]
                if piece == '_':
                    continue
                
                top_piece = self.board[row-1][col]
                bottom_piece = self.board[row+1][col]
                
                # Check if the piece is sandwiched
                if piece in ['A', 'Â'] and top_piece == 'V' and bottom_piece == 'V':
                    pieces_to_remove.append((row, col))
                elif piece == 'V' and top_piece in ['A', 'Â'] and bottom_piece in ['A', 'Â']:
                    pieces_to_remove.append((row, col))
        
        # Remove captured pieces
        for row, col in pieces_to_remove:
            self.board[row][col] = '_'

    def check_win_conditions(self):
        """Check if either player has won"""
        # Check if Â has been captured (Player 1 wins)
        â_exists = False
        for row in self.board:
            if 'Â' in row:
                â_exists = True
                break
        
        if not â_exists:
            self.game_over = True
            self.winner = 1
            return
        
        # Check if Â has reached the border (Player 2 wins)
        for i in range(7):
            # Check top and bottom rows
            if self.board[0][i] == 'Â' or self.board[6][i] == 'Â':
                self.game_over = True
                self.winner = 2
                return
            
            # Check leftmost and rightmost columns
            if self.board[i][0] == 'Â' or self.board[i][6] == 'Â':
                self.game_over = True
                self.winner = 2
                return

    def find_piece_positions(self, player):
        """Return a list of positions for the player's pieces"""
        positions = []
        for row in range(7):
            for col in range(7):
                piece = self.board[row][col]
                if player == 1 and piece == 'V':
                    positions.append((row, col))
                elif player == 2 and piece in ['A', 'Â']:
                    positions.append((row, col))
        return positions

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_input(message, valid_range):
    """Get and validate user input within a range"""
    while True:
        try:
            value = int(input(message))
            if value in valid_range:
                return value
            print(f"Please enter a number between {min(valid_range)} and {max(valid_range)}.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    game = Lilac()
    
    while not game.game_over:
        game.display_board()
        
        # Get player's move
        print(f"Player {game.current_player}'s turn")
        if game.current_player == 1:
            print("You control the V pieces")
        else:
            print("You control the A and Â pieces")
        
        # Show available pieces
        piece_positions = game.find_piece_positions(game.current_player)
        print("Your pieces are at:")
        for i, (row, col) in enumerate(piece_positions):
            piece = game.board[row][col]
            print(f"{i}: {piece} at position ({row}, {col})")
        
        # Get piece selection
        piece_index = get_valid_input("Select a piece (by number): ", range(len(piece_positions)))
        from_row, from_col = piece_positions[piece_index]
        
        # Get move direction
        print("Move direction:")
        print("1: Up")
        print("2: Down")
        print("3: Left")
        print("4: Right")
        direction = get_valid_input("Select direction (1-4): ", range(1, 5))
        
        # Calculate target position
        if direction == 1:  # Up
            to_row, to_col = from_row - 1, from_col
        elif direction == 2:  # Down
            to_row, to_col = from_row + 1, from_col
        elif direction == 3:  # Left
            to_row, to_col = from_row, from_col - 1
        else:  # Right
            to_row, to_col = from_row, from_col + 1
        
        # Attempt to make the move
        if not game.make_move(from_row, from_col, to_row, to_col):
            print("Invalid move. Try again.")
            time.sleep(2)
    
    # Game over
    game.display_board()
    print(f"Game over! Player {game.winner} wins!")
    if game.winner == 1:
        print("Player 1 has captured the special Â piece!")
    else:
        print("Player 2 has moved the special Â piece to the border!")

if __name__ == "__main__":
    main()