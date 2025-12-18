
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    BLACK = 0
    WHITE = 1

class Checkers(Game):
    def __init__(self, board):
        super().__init__(board)
        self.captured_pieces = {Player.BLACK: 0, Player.WHITE: 0}
        self.must_capture = False
        self.current_player_can_capture = False
        self.multi_capture_piece = None
        self.multi_capture_position = None
    
    def initial_player(self):
        return Player.BLACK.value
    
    def prompt_current_player(self):
        player_name = "BLACK" if self.current_player == Player.BLACK.value else "WHITE"
        if self.multi_capture_piece:
            row, col = self.multi_capture_position
            return input(f"Player {player_name}, continue capturing with piece at {row},{col}: ")
        return input(f"Player {player_name}, your move: ")
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        if not is_movement(move):
            return False
        
        (orig_row, orig_col), (dest_row, dest_col) = get_move_elements(move)
        
        # Check if the piece belongs to the current player
        piece = self.board.layout[orig_row, orig_col]
        if self.current_player == Player.BLACK.value and piece != 'b' and piece != 'B':
            return False
        if self.current_player == Player.WHITE.value and piece != 'w' and piece != 'W':
            return False
        
        # If in multi-capture mode, only the piece that just captured can move
        if self.multi_capture_piece:
            if (orig_row, orig_col) != self.multi_capture_position:
                return False
        
        # Check if destination is a blank space
        if self.board.layout[dest_row, dest_col] != '_':
            return False
        
        # Calculate direction and distance
        row_diff = dest_row - orig_row
        col_diff = dest_col - orig_col
        
        # Check if moving diagonally
        if abs(row_diff) != abs(col_diff):
            return False
        
        # Standard pieces can only move forward
        if piece == 'b' and row_diff >= 0:  # Black moves up (decreasing row)
            return False
        if piece == 'w' and row_diff <= 0:  # White moves down (increasing row)
            return False
        
        # Check move distance and if capturing
        distance = abs(row_diff)
        
        # Before checking validity, detect if any captures are possible
        self.current_player_can_capture = self._player_can_capture()
        
        # If player must capture, enforce it
        if self.current_player_can_capture:
            # Must be a capture move
            if distance != 2:
                return False
            
            # Check if there's an opponent's piece to capture
            mid_row = (orig_row + dest_row) // 2
            mid_col = (orig_col + dest_col) // 2
            mid_piece = self.board.layout[mid_row, mid_col]
            
            if self.current_player == Player.BLACK.value:
                if mid_piece != 'w' and mid_piece != 'W':
                    return False
            else:
                if mid_piece != 'b' and mid_piece != 'B':
                    return False
        else:
            # Regular move (no capture)
            if distance > 1:
                return False
        
        return True
    
    def _player_can_capture(self):
        """Check if current player has any capture moves available"""
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                
                # Check if the piece belongs to the current player
                if self.current_player == Player.BLACK.value and piece not in ['b', 'B']:
                    continue
                if self.current_player == Player.WHITE.value and piece not in ['w', 'W']:
                    continue
                
                # Check for possible captures in all diagonal directions
                directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                for dr, dc in directions:
                    # Skip directions that non-king pieces can't move
                    if piece == 'b' and dr > 0:  # Black can only move up
                        continue
                    if piece == 'w' and dr < 0:  # White can only move down
                        continue
                    
                    # Check if there's an opponent's piece and a blank space after it
                    r1, c1 = row + dr, col + dc
                    r2, c2 = row + 2*dr, col + 2*dc
                    
                    if (0 <= r1 < self.board.height and 0 <= c1 < self.board.width and
                        0 <= r2 < self.board.height and 0 <= c2 < self.board.width):
                        
                        mid_piece = self.board.layout[r1, c1]
                        end_cell = self.board.layout[r2, c2]
                        
                        if end_cell == '_':  # Destination is empty
                            if self.current_player == Player.BLACK.value:
                                if mid_piece in ['w', 'W']:  # Can capture white piece
                                    return True
                            else:
                                if mid_piece in ['b', 'B']:  # Can capture black piece
                                    return True
        
        return False

    def _piece_can_capture_more(self, row, col):
        """Check if a specific piece can make more captures"""
        piece = self.board.layout[row, col]
        
        # Check for possible captures in all diagonal directions
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            # Skip directions that non-king pieces can't move
            if piece == 'b' and dr > 0:  # Black can only move up
                continue
            if piece == 'w' and dr < 0:  # White can only move down
                continue
            
            # Check if there's an opponent's piece and a blank space after it
            r1, c1 = row + dr, col + dc
            r2, c2 = row + 2*dr, col + 2*dc
            
            if (0 <= r1 < self.board.height and 0 <= c1 < self.board.width and
                0 <= r2 < self.board.height and 0 <= c2 < self.board.width):
                
                mid_piece = self.board.layout[r1, c1]
                end_cell = self.board.layout[r2, c2]
                
                if end_cell == '_':  # Destination is empty
                    if piece in ['b', 'B']:
                        if mid_piece in ['w', 'W']:  # Can capture white piece
                            return True
                    else:
                        if mid_piece in ['b', 'B']:  # Can capture black piece
                            return True
        
        return False

    def perform_move(self, move):
        (orig_row, orig_col), (dest_row, dest_col) = get_move_elements(move)
        piece = self.board.layout[orig_row, orig_col]
        
        # Check if this is a capture move
        if abs(dest_row - orig_row) == 2:
            # Capture the piece in between
            mid_row = (orig_row + dest_row) // 2
            mid_col = (orig_col + dest_col) // 2
            captured_piece = self.board.layout[mid_row, mid_col]
            
            # Record the capture
            if self.current_player == Player.BLACK.value:
                self.captured_pieces[Player.BLACK] += 1
            else:
                self.captured_pieces[Player.WHITE] += 1
            
            # Remove the captured piece
            self.board.place_piece(f"_ {mid_row},{mid_col}")
            
            # Move the piece
            super().perform_move(move)
            
            # Check for promotion to king
            if (piece == 'b' and dest_row == 0) or (piece == 'w' and dest_row == self.board.height - 1):
                king_piece = 'B' if piece == 'b' else 'W'
                self.board.place_piece(f"{king_piece} {dest_row},{dest_col}")
            
            # Check if the piece can capture more
            if self._piece_can_capture_more(dest_row, dest_col):
                self.multi_capture_piece = self.board.layout[dest_row, dest_col]
                self.multi_capture_position = (dest_row, dest_col)
                self.must_capture = True
            else:
                self.multi_capture_piece = None
                self.multi_capture_position = None
                self.must_capture = False
        else:
            # Regular move
            super().perform_move(move)
            
            # Check for promotion to king
            if (piece == 'b' and dest_row == 0) or (piece == 'w' and dest_row == self.board.height - 1):
                king_piece = 'B' if piece == 'b' else 'W'
                self.board.place_piece(f"{king_piece} {dest_row},{dest_col}")
            
            self.multi_capture_piece = None
            self.multi_capture_position = None
            self.must_capture = False
    
    def next_player(self):
        # If in multi-capture mode, same player continues
        if self.multi_capture_piece:
            return self.current_player
        
        # Otherwise switch players
        if self.current_player == Player.BLACK.value:
            return Player.WHITE.value
        else:
            return Player.BLACK.value
    
    def game_finished(self):
        # Count pieces for each player
        black_pieces = 0
        white_pieces = 0
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                if piece in ['b', 'B']:
                    black_pieces += 1
                elif piece in ['w', 'W']:
                    white_pieces += 1
        
        # Game ends if a player has no pieces left
        if black_pieces == 0 or white_pieces == 0:
            return True
        
        # Or if the current player has no valid moves
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                
                # Check if the piece belongs to the current player
                if self.current_player == Player.BLACK.value and piece not in ['b', 'B']:
                    continue
                if self.current_player == Player.WHITE.value and piece not in ['w', 'W']:
                    continue
                
                # Check for possible moves in all diagonal directions
                directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                for dr, dc in directions:
                    # Skip directions that non-king pieces can't move
                    if piece == 'b' and dr > 0:  # Black can only move up
                        continue
                    if piece == 'w' and dr < 0:  # White can only move down
                        continue
                    
                    # Check for regular move (1 step)
                    r1, c1 = row + dr, col + dc
                    if (0 <= r1 < self.board.height and 0 <= c1 < self.board.width and
                        self.board.layout[r1, c1] == '_'):
                        return False  # Player can make a move
                    
                    # Check for capture move (2 steps)
                    r2, c2 = row + 2*dr, col + 2*dc
                    if (0 <= r1 < self.board.height and 0 <= c1 < self.board.width and
                        0 <= r2 < self.board.height and 0 <= c2 < self.board.width):
                        
                        mid_piece = self.board.layout[r1, c1]
                        end_cell = self.board.layout[r2, c2]
                        
                        if end_cell == '_':  # Destination is empty
                            if self.current_player == Player.BLACK.value:
                                if mid_piece in ['w', 'W']:  # Can capture white piece
                                    return False  # Player can make a move
                            else:
                                if mid_piece in ['b', 'B']:  # Can capture black piece
                                    return False  # Player can make a move
        
        # No valid moves found
        return True
    
    def get_winner(self):
        # Count pieces for each player
        black_pieces = 0
        white_pieces = 0
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                if piece in ['b', 'B']:
                    black_pieces += 1
                elif piece in ['w', 'W']:
                    white_pieces += 1
        
        if black_pieces == 0:
            return Player.WHITE.value
        if white_pieces == 0:
            return Player.BLACK.value
        
        # If current player has no valid moves, opponent wins
        return Player.WHITE.value if self.current_player == Player.BLACK.value else Player.BLACK.value
    
    def finish_message(self, winner):
        player_name = "BLACK" if winner == Player.BLACK.value else "WHITE"
        print(f"Player {player_name} wins!")
        print(f"BLACK captured {self.captured_pieces[Player.BLACK]} pieces")
        print(f"WHITE captured {self.captured_pieces[Player.WHITE]} pieces")

    def get_state(self):
        state = super().get_state()
        additional_params = state[2]
        additional_params.extend([
            self.captured_pieces,
            self.must_capture,
            self.multi_capture_piece,
            self.multi_capture_position
        ])
        return (state[0], state[1], additional_params)

if __name__ == '__main__':
    # Create the initial checkers board layout
    layout = ""
    for i in range(8):
        for j in range(8):
            if i < 3 and (i + j) % 2 == 1:
                layout += "w"  # White pieces at the top
            elif i > 4 and (i + j) % 2 == 1:
                layout += "b"  # Black pieces at the bottom
            elif (i + j) % 2 == 1:
                layout += "_"  # Empty playable spaces
            else:
                layout += " "  # Non-playable spaces
        if i < 7:
            layout += "\n"
    
    board = Board((8, 8), layout)
    checkers = Checkers(board)
    checkers.game_loop()
