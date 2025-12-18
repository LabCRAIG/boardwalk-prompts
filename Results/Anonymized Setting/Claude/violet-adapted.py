from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from enum import IntEnum

class Player(IntEnum):
    ONE = 0  # Player 1 (A)
    TWO = 1  # Player 2 (V)

class Violet(Game):
    def __init__(self, board):
        super().__init__(board)
        self.piece_map = {
            Player.ONE: 'A',
            Player.TWO: 'V'
        }
        self.last_moved_position = None
    
    def initial_player(self):
        return Player.ONE
    
    def prompt_current_player(self):
        player_piece = self.piece_map[self.current_player]
        print(f"\nPlayer {int(self.current_player) + 1}'s turn ({player_piece})")
        
        # Find all pieces for the current player
        pieces = []
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == player_piece:
                    pieces.append((row, col))
        
        if not pieces:
            return ""  # No pieces left
        
        # Show available pieces
        print("Your pieces are at:")
        for i, (row, col) in enumerate(pieces):
            print(f"{i+1}: Position ({row}, {col})")
        
        # Get piece selection
        valid_selection = False
        selected_pos = None
        valid_moves = []
        
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
        
        # Get move selection
        valid_move = False
        destination = None
        
        while not valid_move:
            try:
                move_selection = int(input("Select a destination (enter the number): ")) - 1
                if 0 <= move_selection < len(valid_moves):
                    destination = valid_moves[move_selection]
                    valid_move = True
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Format the move string according to the API's standard move format
        move_str = f"{selected_pos[0]},{selected_pos[1]} {destination[0]},{destination[1]}"
        self.last_moved_position = destination
        
        return move_str
    
    def perform_move(self, move):
        # First, perform the piece movement
        super().perform_move(move)
        
        # Now handle the X shot part
        if self.last_moved_position:
            row, col = self.last_moved_position
            valid_shots = self.get_valid_moves(row, col)
            
            # Display valid shots
            print("Valid shots for X:")
            for i, (shot_row, shot_col) in enumerate(valid_shots):
                print(f"{i+1}: Position ({shot_row}, {shot_col})")
            
            # Get shot selection
            valid_shot = False
            shot_pos = None
            
            while not valid_shot:
                try:
                    shot_selection = int(input("Select where to place X (enter the number): ")) - 1
                    if 0 <= shot_selection < len(valid_shots):
                        shot_pos = valid_shots[shot_selection]
                        valid_shot = True
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Format the shot placement according to API's standard placement format
            shot_move = f"X {shot_pos[0]},{shot_pos[1]}"
            self.board.place_piece(shot_move)
    
    def get_valid_moves(self, row, col):
        """Get all valid moves for piece at (row, col)"""
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
                if not (0 <= r < self.board.height and 0 <= c < self.board.width):
                    break
                # Check if position is free (using the BLANK character '_')
                if self.board.layout[r, c] == '_':
                    valid_moves.append((r, c))
                else:
                    break
        
        return valid_moves
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        # Ensure it's a movement, not a placement
        if not is_movement(move):
            return False
        
        # Get origin and destination
        origin, destination = get_move_elements(move)
        
        # Check that origin has the correct piece for current player
        origin_row, origin_col = origin
        if self.board.layout[origin_row, origin_col] != self.piece_map[self.current_player]:
            return False
        
        # Check that destination is empty
        dest_row, dest_col = destination
        if self.board.layout[dest_row, dest_col] != '_':
            return False
        
        # Check that the move follows piece movement rules (straight line, no pieces in between)
        valid_moves = self.get_valid_moves(origin_row, origin_col)
        if (dest_row, dest_col) not in valid_moves:
            return False
        
        return True
    
    def game_finished(self):
        # Check if current player has any valid moves
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == self.piece_map[self.current_player]:
                    if self.get_valid_moves(row, col):
                        return False
        
        # If we get here, current player has no valid moves
        return True
    
    def get_winner(self):
        # The winner is the other player
        return Player.TWO if self.current_player == Player.ONE else Player.ONE
    
    def next_player(self):
        # Switch players: 0->1, 1->0
        return Player.TWO if self.current_player == Player.ONE else Player.ONE
    
    def finish_message(self, winner):
        winner_piece = self.piece_map[winner]
        print(f"Player {int(winner) + 1} ({winner_piece}) wins!")
        print("The other player has no valid moves left.")

if __name__ == '__main__':
    # Create initial layout string for the Board
    layout = np.full((10, 10), '_', dtype=str)  # All blank spaces
    
    # Set Player 1 (A) pieces
    layout[6, 0] = 'A'
    layout[6, 9] = 'A'
    layout[9, 3] = 'A'
    layout[9, 6] = 'A'
    
    # Set Player 2 (V) pieces
    layout[0, 3] = 'V'
    layout[0, 6] = 'V'
    layout[3, 0] = 'V'
    layout[3, 9] = 'V'
    
    # Convert layout to string format required by Board constructor
    layout_str = '\n'.join(''.join(row) for row in layout)
    
    # Initialize board and game
    board = Board((10, 10), layout_str)
    violet_game = Violet(board)
    
    print("Welcome to Violet!")
    print("Player 1 controls A pieces, Player 2 controls V pieces")
    print("On your turn, move one of your pieces and then shoot an X")
    print("Win by blocking your opponent so they can't move")
    
    violet_game.game_loop()
