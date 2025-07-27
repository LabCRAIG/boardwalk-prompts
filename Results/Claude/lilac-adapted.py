from game import Game, Board, is_movement, is_placement, get_move_elements
import os
from enum import IntEnum

class Player(IntEnum):
    ONE = 0  # Player 1 (V's)
    TWO = 1  # Player 2 (A's and Â)

class LilacGame(Game):
    def __init__(self, board):
        super().__init__(board)
        self.game_over = False
        self.winner = None

    def initial_player(self):
        return Player.ONE  # Player 1 starts (V's)

    def validate_move(self, move):
        # First check if the move is properly formatted and within board bounds
        if not super().validate_move(move):
            return False
        
        if not is_movement(move):
            return False  # Only movement is allowed, not placement
        
        # Get the origin and destination coordinates
        origin, dest = get_move_elements(move)
        from_row, from_col = origin
        to_row, to_col = dest
        
        # Check if the "from" position contains the current player's piece
        piece = self.board.layout[from_row][from_col]
        if self.current_player == Player.ONE and piece != 'V':
            return False
        if self.current_player == Player.TWO and piece not in ['A', 'Â']:
            return False
        
        # Check if the "to" position is empty
        if self.board.layout[to_row][to_col] != '_':
            return False
        
        # Check if move is orthogonal and only one space
        if (from_row == to_row and abs(from_col - to_col) == 1) or \
           (from_col == to_col and abs(from_row - to_row) == 1):
            # Check the center rule - only Â can occupy the center
            if to_row == 3 and to_col == 3 and piece != 'Â':
                return False
            return True
        
        return False

    def perform_move(self, move):
        # Call the parent method to perform the basic movement
        super().perform_move(move)
        
        # Check for captures after the move
        self.check_captures()
        
        # Check win conditions
        if self.game_finished():
            self.game_over = True

    def check_captures(self):
        """Check for sandwiched pieces and remove them"""
        pieces_to_remove = []
        
        # Check horizontally
        for row in range(7):
            for col in range(1, 6):  # Skip edges since they can't be sandwiched
                piece = self.board.layout[row][col]
                if piece == '_':
                    continue
                
                left_piece = self.board.layout[row][col-1]
                right_piece = self.board.layout[row][col+1]
                
                # Check if the piece is sandwiched
                if piece in ['A', 'Â'] and left_piece == 'V' and right_piece == 'V':
                    pieces_to_remove.append((row, col))
                elif piece == 'V' and left_piece in ['A', 'Â'] and right_piece in ['A', 'Â']:
                    pieces_to_remove.append((row, col))
        
        # Check vertically
        for col in range(7):
            for row in range(1, 6):  # Skip edges
                piece = self.board.layout[row][col]
                if piece == '_':
                    continue
                
                top_piece = self.board.layout[row-1][col]
                bottom_piece = self.board.layout[row+1][col]
                
                # Check if the piece is sandwiched
                if piece in ['A', 'Â'] and top_piece == 'V' and bottom_piece == 'V':
                    pieces_to_remove.append((row, col))
                elif piece == 'V' and top_piece in ['A', 'Â'] and bottom_piece in ['A', 'Â']:
                    pieces_to_remove.append((row, col))
        
        # Remove captured pieces
        for row, col in pieces_to_remove:
            self.board.layout[row][col] = '_'

    def game_finished(self):
        """Check if either player has won"""
        # Check if Â has been captured (Player 1 wins)
        â_exists = False
        for row in self.board.layout:
            if 'Â' in row:
                â_exists = True
                break
        
        if not â_exists:
            self.winner = Player.ONE
            return True
        
        # Check if Â has reached the border (Player 2 wins)
        for i in range(7):
            # Check top and bottom rows
            if self.board.layout[0][i] == 'Â' or self.board.layout[6][i] == 'Â':
                self.winner = Player.TWO
                return True
            
            # Check leftmost and rightmost columns
            if self.board.layout[i][0] == 'Â' or self.board.layout[i][6] == 'Â':
                self.winner = Player.TWO
                return True
        
        return False

    def get_winner(self):
        """Return the winner of the game"""
        return self.winner

    def next_player(self):
        """Alternates between players 1 and 2"""
        return Player.TWO if self.current_player == Player.ONE else Player.ONE

    def prompt_current_player(self):
        """Custom prompt for the player to make a move"""
        clear_screen()
        print(f"Player {int(self.current_player) + 1}'s turn")
        
        if self.current_player == Player.ONE:
            print("You control the V pieces")
        else:
            print("You control the A and Â pieces")
        
        # Show available pieces
        piece_positions = self.find_piece_positions()
        print("Your pieces are at:")
        for i, (row, col) in enumerate(piece_positions):
            piece = self.board.layout[row][col]
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
        
        # Return the move in standard format
        return f"{from_row},{from_col} {to_row},{to_col}"

    def find_piece_positions(self):
        """Return a list of positions for the current player's pieces"""
        positions = []
        for row in range(7):
            for col in range(7):
                piece = self.board.layout[row][col]
                if self.current_player == Player.ONE and piece == 'V':
                    positions.append((row, col))
                elif self.current_player == Player.TWO and piece in ['A', 'Â']:
                    positions.append((row, col))
        return positions

    def finish_message(self, winner):
        """Display a custom message at the end of the game"""
        print(f"Game over! Player {int(winner) + 1} wins!")
        if winner == Player.ONE:
            print("Player 1 has captured the special Â piece!")
        else:
            print("Player 2 has moved the special Â piece to the border!")

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

if __name__ == '__main__':
    # Initial layout of the board
    initial_layout = """__VVV__
___V___
V_AAA_V
VVAÂAVV
V_AAA_V
___V___
__VVV__"""
    
    # Create board and game
    board = Board((7, 7), initial_layout)
    lilac_game = LilacGame(board)
    
    # Start the game
    lilac_game.game_loop()