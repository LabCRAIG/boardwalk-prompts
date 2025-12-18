from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from copy import deepcopy

class Lazuli(Game):
    def __init__(self, board):
        super().__init__(board)
        # No additional attributes needed as the game state is fully 
        # represented by the board layout

    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        # Only allow movement-type moves
        if not is_movement(move):
            return False
            
        # Get the origin and destination coordinates
        origin, destination = get_move_elements(move)
        from_row, from_col = origin
        to_row, to_col = destination
        
        # Check if origin has a piece
        if self.board.layout[from_row, from_col] != 'X':
            return False
            
        # Check if destination is empty
        if self.board.layout[to_row, to_col] != '_':
            return False
            
        # Calculate the position of the jumped piece
        jumped_row = (from_row + to_row) // 2
        jumped_col = (from_col + to_col) // 2
        
        # Check if the jump is valid:
        # 1. Must be horizontal or vertical (not diagonal)
        if from_row != to_row and from_col != to_col:
            return False
            
        # 2. Must be exactly 2 spaces away
        if abs(from_row - to_row) + abs(from_col - to_col) != 2:
            return False
            
        # 3. Must have a piece to jump over
        if self.board.layout[jumped_row, jumped_col] != 'X':
            return False
            
        return True

    def perform_move(self, move):
        # Extract the move coordinates
        origin, destination = get_move_elements(move)
        from_row, from_col = origin
        to_row, to_col = destination
        
        # Calculate the position of the jumped piece
        jumped_row = (from_row + to_row) // 2
        jumped_col = (from_col + to_col) // 2
        
        # Move the piece using the API
        self.board.move_piece(move)
        
        # Remove the jumped piece by placing a blank
        jump_move = f"_ {jumped_row},{jumped_col}"
        self.board.place_piece(jump_move)

    def game_finished(self):
        # Count remaining pieces
        piece_count = np.sum(self.board.layout == 'X')
        
        # Check win condition: only one piece left at the center
        if piece_count == 1 and self.board.layout[3, 3] == 'X':
            return True
            
        # Check if there are no valid moves left
        for row in range(7):
            for col in range(7):
                if self.board.layout[row, col] == 'X':
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
                            self.board.layout[jump_row, jump_col] == 'X' and
                            self.board.layout[landing_row, landing_col] == '_'):
                            return False
        
        return True

    def get_winner(self):
        # Count remaining pieces
        piece_count = np.sum(self.board.layout == 'X')
        
        # The player wins if there's only one piece left and it's at the center
        if piece_count == 1 and self.board.layout[3, 3] == 'X':
            return 1
        else:
            return None

    def next_player(self):
        # Single player game, so always return the same player
        return 1
        
    def prompt_current_player(self):
        print(f"Valid moves:")
        
        # Generate and display valid moves
        valid_moves = []
        
        for row in range(7):
            for col in range(7):
                if self.board.layout[row, col] == 'X':
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
                            self.board.layout[jump_row, jump_col] == 'X' and
                            self.board.layout[landing_row, landing_col] == '_'):
                            valid_moves.append((row, col, landing_row, landing_col))
        
        # Display available moves
        for i, (fr, fc, tr, tc) in enumerate(valid_moves):
            print(f"{i+1}. Move from ({fr},{fc}) to ({tr},{tc})")
        
        # Get player choice
        try:
            choice = int(input("Enter move number: ")) - 1
            if 0 <= choice < len(valid_moves):
                from_row, from_col, to_row, to_col = valid_moves[choice]
                return f"{from_row},{from_col} {to_row},{to_col}"
            else:
                print("Invalid choice. Please try again.")
                return self.prompt_current_player()
        except ValueError:
            print("Please enter a valid number.")
            return self.prompt_current_player()
    
    def finish_message(self, winner):
        if winner is not None:
            print("Congratulations! You won!")
        else:
            print("Game over. You lost!")
    
    def initial_player(self):
        return 1


def create_initial_board():
    # Create the initial layout string
    layout_rows = []
    
    # Mark null spaces (2x2 corners) and fill the rest with X's (except center)
    for row in range(7):
        row_str = ""
        for col in range(7):
            # Check if position is in a corner
            is_corner = ((row < 2 and col < 2) or  # Top-left corner
                         (row < 2 and col > 4) or  # Top-right corner
                         (row > 4 and col < 2) or  # Bottom-left corner
                         (row > 4 and col > 4))    # Bottom-right corner
            
            # Center position
            is_center = (row == 3 and col == 3)
            
            if is_corner:
                row_str += " "  # Null space
            elif is_center:
                row_str += "_"  # Empty space
            else:
                row_str += "X"  # Piece
        
        layout_rows.append(row_str)
    
    return "\n".join(layout_rows)


if __name__ == '__main__':
    # Create the initial board layout
    initial_layout = create_initial_board()
    board = Board((7, 7), initial_layout)
    
    # Initialize and start the game
    print("Welcome to Lazuli!")
    print("The goal is to have only one piece left, and it must be in the center.")
    
    lazuli_game = Lazuli(board)
    lazuli_game.game_loop()