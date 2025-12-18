
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    ONE = 1
    TWO = 2

class Checkers(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = self.initial_player()
        # Pieces are represented as 'r' for red (player 1) and 'b' for black (player 2)
        # Kings are represented as 'R' for red and 'B' for black
        self.capture_available = False

    def initial_player(self):
        return Player.ONE

    def prompt_current_player(self):
        player_name = "Red" if self.current_player == Player.ONE else "Black"
        return input(f"{player_name}'s move: ")

    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        # Only movements are allowed in checkers
        if not is_movement(move):
            return False
            
        origin, destination = get_move_elements(move)
        
        # Check if origin has the player's piece
        piece_at_origin = self.board.layout[origin[0], origin[1]]
        if self.current_player == Player.ONE and piece_at_origin not in ['r', 'R']:
            return False
        if self.current_player == Player.TWO and piece_at_origin not in ['b', 'B']:
            return False
            
        # Check if destination is empty
        if self.board.layout[destination[0], destination[1]] != '_':
            return False
            
        # Check if the move is diagonal
        row_diff = destination[0] - origin[0]
        col_diff = destination[1] - origin[1]
        
        # Must be diagonal move
        if abs(row_diff) != abs(col_diff):
            return False
            
        # Regular pieces can only move forward
        if piece_at_origin == 'r' and row_diff >= 0:
            return False
        if piece_at_origin == 'b' and row_diff <= 0:
            return False
            
        # Handle single step moves
        if abs(row_diff) == 1:
            # If there's a capture available, player must capture
            if self.capture_available:
                return False
            return True
            
        # Handle captures (jumps of 2 spaces)
        if abs(row_diff) == 2:
            # Check if there's an opponent's piece in between
            middle_row = origin[0] + (row_diff // 2)
            middle_col = origin[1] + (col_diff // 2)
            middle_piece = self.board.layout[middle_row, middle_col]
            
            if self.current_player == Player.ONE and middle_piece not in ['b', 'B']:
                return False
            if self.current_player == Player.TWO and middle_piece not in ['r', 'R']:
                return False
                
            return True
            
        # No other move distances allowed
        return False

    def can_capture(self, player):
        height, width = self.board.layout.shape
        
        player_pieces = ['r', 'R'] if player == Player.ONE else ['b', 'B']
        opponent_pieces = ['b', 'B'] if player == Player.ONE else ['r', 'R']
        
        for row in range(height):
            for col in range(width):
                if self.board.layout[row, col] in player_pieces:
                    # Check all 4 possible diagonal capture directions
                    directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
                    
                    # Regular pieces can only move in certain directions
                    if self.board.layout[row, col] == 'r':  # Only downward
                        directions = [(-2, 2), (-2, -2)]
                    elif self.board.layout[row, col] == 'b':  # Only upward
                        directions = [(2, 2), (2, -2)]
                    
                    for dr, dc in directions:
                        target_row, target_col = row + dr, col + dc
                        middle_row, middle_col = row + (dr // 2), col + (dc // 2)
                        
                        # Check bounds
                        if 0 <= target_row < height and 0 <= target_col < width:
                            # Check if middle has opponent's piece and target is empty
                            if (self.board.layout[middle_row, middle_col] in opponent_pieces and 
                                self.board.layout[target_row, target_col] == '_'):
                                return True
        return False

    def perform_move(self, move):
        origin, destination = get_move_elements(move)
        piece = self.board.layout[origin[0], origin[1]]
        
        # Check if it's a capture move
        row_diff = destination[0] - origin[0]
        col_diff = destination[1] - origin[1]
        
        if abs(row_diff) == 2:  # Capture move
            # Remove captured piece
            middle_row = origin[0] + (row_diff // 2)
            middle_col = origin[1] + (col_diff // 2)
            self.board.place_piece(f"_ {middle_row},{middle_col}")
        
        # Execute the move
        super().perform_move(move)
        
        # Check for promotion to king
        height = self.board.layout.shape[0]
        if (piece == 'r' and destination[0] == 0) or (piece == 'b' and destination[0] == height - 1):
            # Promote to king
            king_piece = 'R' if piece == 'r' else 'B'
            self.board.place_piece(f"{king_piece} {destination[0]},{destination[1]}")
        
        # Check if multiple captures are available
        self.capture_available = False
        if abs(row_diff) == 2:  # If this was a capture
            # Create a temporary copy of the board state to check for more captures
            temp_layout = deepcopy(self.board.layout)
            temp_piece = temp_layout[destination[0], destination[1]]
            
            # Check if the piece that just moved can capture again
            directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
            if temp_piece == 'r':  # Regular red piece can only move up
                directions = [(-2, 2), (-2, -2)]
            elif temp_piece == 'b':  # Regular black piece can only move down
                directions = [(2, 2), (2, -2)]
            
            opponent_pieces = ['b', 'B'] if self.current_player == Player.ONE else ['r', 'R']
            height, width = self.board.layout.shape
            
            for dr, dc in directions:
                target_row, target_col = destination[0] + dr, destination[1] + dc
                middle_row, middle_col = destination[0] + (dr // 2), destination[1] + (dc // 2)
                
                if 0 <= target_row < height and 0 <= target_col < width:
                    if (temp_layout[middle_row, middle_col] in opponent_pieces and
                        temp_layout[target_row, target_col] == '_'):
                        self.capture_available = True
                        return  # Don't change player if another capture is available
        
    def next_player(self):
        if self.capture_available:
            return self.current_player
        return Player.TWO if self.current_player == Player.ONE else Player.ONE

    def game_finished(self):
        red_pieces = 0
        black_pieces = 0
        
        for row in range(self.board.layout.shape[0]):
            for col in range(self.board.layout.shape[1]):
                piece = self.board.layout[row, col]
                if piece in ['r', 'R']:
                    red_pieces += 1
                elif piece in ['b', 'B']:
                    black_pieces += 1
        
        # Game is over if one player has no pieces left
        if red_pieces == 0 or black_pieces == 0:
            return True
            
        # Check if current player has valid moves
        player_pieces = ['r', 'R'] if self.current_player == Player.ONE else ['b', 'B']
        height, width = self.board.layout.shape
        
        for row in range(height):
            for col in range(width):
                if self.board.layout[row, col] in player_pieces:
                    piece = self.board.layout[row, col]
                    directions = []
                    
                    # Define possible move directions based on piece type
                    if piece == 'r':
                        directions = [(-1, -1), (-1, 1)]  # Regular red piece moves up
                    elif piece == 'b':
                        directions = [(1, -1), (1, 1)]    # Regular black piece moves down
                    else:  # Kings can move in all diagonal directions
                        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                    
                    # Check for single step moves
                    for dr, dc in directions:
                        target_row, target_col = row + dr, col + dc
                        if 0 <= target_row < height and 0 <= target_col < width:
                            if self.board.layout[target_row, target_col] == '_':
                                return False  # Valid move exists
                    
                    # Check for capture moves
                    capture_directions = []
                    if piece == 'r':
                        capture_directions = [(-2, -2), (-2, 2)]
                    elif piece == 'b':
                        capture_directions = [(2, -2), (2, 2)]
                    else:  # Kings
                        capture_directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
                    
                    opponent_pieces = ['b', 'B'] if self.current_player == Player.ONE else ['r', 'R']
                    
                    for dr, dc in capture_directions:
                        target_row, target_col = row + dr, col + dc
                        middle_row, middle_col = row + (dr // 2), col + (dc // 2)
                        
                        if 0 <= target_row < height and 0 <= target_col < width:
                            if (self.board.layout[middle_row, middle_col] in opponent_pieces and
                                self.board.layout[target_row, target_col] == '_'):
                                return False  # Valid capture exists
        
        return True  # No valid moves
        
    def get_winner(self):
        red_pieces = 0
        black_pieces = 0
        
        for row in range(self.board.layout.shape[0]):
            for col in range(self.board.layout.shape[1]):
                piece = self.board.layout[row, col]
                if piece in ['r', 'R']:
                    red_pieces += 1
                elif piece in ['b', 'B']:
                    black_pieces += 1
        
        if red_pieces == 0:
            return Player.TWO
        if black_pieces == 0:
            return Player.ONE
            
        # If current player has no valid moves, opponent wins
        return Player.TWO if self.current_player == Player.ONE else Player.ONE
    
    def finish_message(self, winner):
        winner_name = "Red" if winner == Player.ONE else "Black"
        print(f"{winner_name} wins the game!")

if __name__ == '__main__':
    # Create initial layout for checkers
    rows, cols = 8, 8
    layout = ""
    
    # Fill the first two rows with player 2 pieces (black)
    for i in range(2):
        for j in range(cols):
            layout += "b"
        if i < 1:  # Add newline except for the last row
            layout += "\n"
            
    # Fill the middle 4 rows with empty spaces
    for i in range(4):
        layout += "\n"
        for j in range(cols):
            layout += "_"
            
    # Fill the last two rows with player 1 pieces (red)
    for i in range(2):
        layout += "\n"
        for j in range(cols):
            layout += "r"
    
    board = Board((rows, cols), layout)
    mygame = Checkers(board)
    mygame.game_loop()
