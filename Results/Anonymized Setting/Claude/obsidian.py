from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
import numpy as np
from copy import deepcopy

# Enum for players
class Player(Enum):
    ONE = 0  # Lowercase pieces
    TWO = 1  # Uppercase pieces

class Obsidian(Game):
    def __init__(self, board):
        super().__init__(board)
        self.f_moved = {}  # Track if F/f pieces have moved (for two-space first move)
        
    def initial_player(self):
        return Player.ONE.value
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        # Must be a movement, not a placement
        if not is_movement(move):
            return False
            
        # Extract origin and destination
        origin, destination = get_move_elements(move)
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        # Check if origin has player's piece
        piece = self.board.layout[origin_row, origin_col]
        if piece == '_' or piece == ' ':
            return False
            
        # Check if current player is controlling the right pieces
        if self.current_player == Player.ONE.value and not piece.islower():
            return False
        if self.current_player == Player.TWO.value and not piece.isupper():
            return False
            
        # Check if destination is empty or has opponent's piece
        dest_piece = self.board.layout[dest_row, dest_col]
        if dest_piece != '_':
            if dest_piece == ' ':
                return False  # Can't move to NULL space
            if self.current_player == Player.ONE.value and dest_piece.islower():
                return False  # Can't capture own pieces
            if self.current_player == Player.TWO.value and dest_piece.isupper():
                return False  # Can't capture own pieces
        
        # Validate piece-specific movement
        if piece.lower() == 'f':
            return self._validate_f_move(piece, origin, destination, dest_piece)
        elif piece.lower() == 'a':
            return self._validate_a_move(piece, origin, destination, dest_piece)
        elif piece.lower() == 'c':
            return self._validate_c_move(piece, origin, destination, dest_piece)
        elif piece.lower() == 'b':
            return self._validate_b_move(piece, origin, destination, dest_piece)
        elif piece.lower() == 'e':
            return self._validate_e_move(piece, origin, destination, dest_piece)
        elif piece.lower() == 'd':
            return self._validate_d_move(piece, origin, destination, dest_piece)
            
        return False
    
    def _validate_f_move(self, piece, origin, destination, dest_piece):
        """Validate F/f piece movement"""
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        is_lowercase = piece.islower()
        forward_dir = -1 if is_lowercase else 1  # Direction of "forward" movement
        
        # Check if moving forward
        if forward_dir == -1 and dest_row > origin_row:
            return False
        if forward_dir == 1 and dest_row < origin_row:
            return False
            
        row_diff = abs(dest_row - origin_row)
        col_diff = abs(dest_col - origin_col)
        
        # Diagonal capture
        if col_diff == 1 and row_diff == 1:
            if forward_dir * (dest_row - origin_row) > 0:  # Not moving forward
                return False
            return dest_piece != '_'  # Must be capturing
            
        # Straight forward movement
        if col_diff != 0:
            return False
        
        # Check distance
        if row_diff > 2:
            return False
        if row_diff == 2:
            # Check if first move for this piece
            piece_key = f"{origin_row},{origin_col}"
            if piece_key in self.f_moved and self.f_moved[piece_key]:
                return False
            # Check if path is clear
            mid_row = origin_row + forward_dir
            if self.board.layout[mid_row, origin_col] != '_':
                return False
        
        # Destination must be empty for forward movement
        return dest_piece == '_'
        
    def _validate_a_move(self, piece, origin, destination, dest_piece):
        """Validate A/a piece movement (rook-like, orthogonal movement)"""
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        # Must move orthogonally
        if origin_row != dest_row and origin_col != dest_col:
            return False
            
        # Check if path is clear
        if origin_row == dest_row:  # Horizontal move
            step = 1 if dest_col > origin_col else -1
            for col in range(origin_col + step, dest_col, step):
                if self.board.layout[origin_row, col] != '_':
                    return False
        else:  # Vertical move
            step = 1 if dest_row > origin_row else -1
            for row in range(origin_row + step, dest_row, step):
                if self.board.layout[row, origin_col] != '_':
                    return False
                    
        return True
        
    def _validate_c_move(self, piece, origin, destination, dest_piece):
        """Validate C/c piece movement (bishop-like, diagonal movement)"""
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        row_diff = abs(dest_row - origin_row)
        col_diff = abs(dest_col - origin_col)
        
        # Must move diagonally
        if row_diff != col_diff:
            return False
            
        # Check if path is clear
        row_step = 1 if dest_row > origin_row else -1
        col_step = 1 if dest_col > origin_col else -1
        
        for i in range(1, row_diff):
            if self.board.layout[origin_row + i * row_step, origin_col + i * col_step] != '_':
                return False
                
        return True
        
    def _validate_b_move(self, piece, origin, destination, dest_piece):
        """Validate B/b piece movement (knight-like, L-shaped movement)"""
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        row_diff = abs(dest_row - origin_row)
        col_diff = abs(dest_col - origin_col)
        
        # Knight-like movement: 2 in one direction, 1 in orthogonal direction
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
        
    def _validate_e_move(self, piece, origin, destination, dest_piece):
        """Validate E/e piece movement (queen-like, any direction)"""
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        row_diff = abs(dest_row - origin_row)
        col_diff = abs(dest_col - origin_col)
        
        # Can move diagonally
        if row_diff == col_diff:
            return self._validate_c_move(piece, origin, destination, dest_piece)
            
        # Can move orthogonally
        if origin_row == dest_row or origin_col == dest_col:
            return self._validate_a_move(piece, origin, destination, dest_piece)
            
        return False
        
    def _validate_d_move(self, piece, origin, destination, dest_piece):
        """Validate D/d piece movement (king-like, one space in any direction)"""
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        row_diff = abs(dest_row - origin_row)
        col_diff = abs(dest_col - origin_col)
        
        # One space in any direction
        return row_diff <= 1 and col_diff <= 1 and (row_diff > 0 or col_diff > 0)
        
    def perform_move(self, move):
        # Get move details before performing it
        origin, destination = get_move_elements(move)
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        piece = self.board.layout[origin_row, origin_col]
        
        # Track if F/f has moved
        if piece.lower() == 'f':
            piece_key = f"{origin_row},{origin_col}"
            self.f_moved[piece_key] = True
        
        # Perform the basic move
        super().perform_move(move)
        
        # F/f promotion when reaching the opposite edge
        if piece == 'f' and dest_row == 0:  # Lowercase f reaches top row
            self.board.place_piece(f"e {dest_row},{dest_col}")
        elif piece == 'F' and dest_row == 7:  # Uppercase F reaches bottom row
            self.board.place_piece(f"E {dest_row},{dest_col}")
    
    def game_finished(self):
        # Check if any player's D/d is captured
        p1_d_exists = False
        p2_d_exists = False
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                if piece == 'd':
                    p1_d_exists = True
                elif piece == 'D':
                    p2_d_exists = True
        
        return not (p1_d_exists and p2_d_exists)
    
    def get_winner(self):
        # If game is finished, determine the winner
        if not self.game_finished():
            return None
            
        # Check if each player's king exists
        p1_d_exists = False
        p2_d_exists = False
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                if piece == 'd':
                    p1_d_exists = True
                elif piece == 'D':
                    p2_d_exists = True
        
        if p1_d_exists and not p2_d_exists:
            return Player.ONE.value
        if p2_d_exists and not p1_d_exists:
            return Player.TWO.value
            
        return None  # Should not happen with current rules
    
    def next_player(self):
        # Alternate between players
        return (self.current_player + 1) % 2
        
    def finish_message(self, winner):
        if winner == Player.ONE.value:
            print("Player 1 (lowercase) wins!")
        elif winner == Player.TWO.value:
            print("Player 2 (UPPERCASE) wins!")
        else:
            print("The game ended in a draw.")

if __name__ == '__main__':
    # Set up initial board layout
    initial_layout = (
        "ABCDECBA\n" +
        "FFFFFFFF\n" +
        "________\n" +
        "________\n" +
        "________\n" +
        "________\n" +
        "ffffffff\n" +
        "abcdecba"
    )
    
    board = Board((8, 8), initial_layout)
    game = Obsidian(board)
    game.game_loop()