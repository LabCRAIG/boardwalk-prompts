from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from enum import Enum

class Player(Enum):
    RED = 0
    BLACK = 1

class Checkers(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = self.initial_player()
        self.capture_chain = None
        
    def initial_player(self):
        return Player.RED.value
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        try:
            if is_movement(move):
                (from_pos, to_pos) = get_move_elements(move)
                from_row, from_col = from_pos
                to_row, to_col = to_pos
                
                # Check if moving own piece
                piece = self.board.layout[from_row, from_col]
                if self.current_player == Player.RED.value and piece not in ['r', 'R']:
                    return False
                if self.current_player == Player.BLACK.value and piece not in ['b', 'B']:
                    return False
                    
                # Check if destination is blank
                if self.board.layout[to_row, to_col] != '_':
                    return False
                    
                # Check valid movement pattern
                row_diff = to_row - from_row
                col_diff = to_col - from_col
                
                # Kings can move both directions
                if piece in ['R', 'B']:
                    direction_valid = abs(row_diff) == 1 and abs(col_diff) == 1
                    capture_valid = abs(row_diff) == 2 and abs(col_diff) == 2
                else:
                    # Regular pieces can only move forward
                    if self.current_player == Player.RED.value:
                        direction_valid = row_diff == -1 and abs(col_diff) == 1
                        capture_valid = row_diff == -2 and abs(col_diff) == 2
                    else:
                        direction_valid = row_diff == 1 and abs(col_diff) == 1
                        capture_valid = row_diff == 2 and abs(col_diff) == 2
                
                # Check for captures
                if capture_valid:
                    jump_row = (from_row + to_row) // 2
                    jump_col = (from_col + to_col) // 2
                    jumped_piece = self.board.layout[jump_row, jump_col]
                    
                    # Check if jumping opponent piece
                    if self.current_player == Player.RED.value and jumped_piece not in ['b', 'B']:
                        return False
                    if self.current_player == Player.BLACK.value and jumped_piece not in ['r', 'R']:
                        return False
                    return True
                    
                return direction_valid and not self.has_available_captures()
                
            return False
        except:
            return False
            
    def has_available_captures(self):
        # Check if current player has any available captures
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                if (self.current_player == Player.RED.value and piece in ['r', 'R']) or \
                   (self.current_player == Player.BLACK.value and piece in ['b', 'B']):
                   
                    # Check all possible capture moves
                    for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                        if piece in ['r', 'R'] or (piece == 'r' and dr == -2) or (piece == 'b' and dr == 2):
                            to_row, to_col = row + dr, col + dc
                            if 0 <= to_row < self.board.height and 0 <= to_col < self.board.width:
                                if self.board.layout[to_row, to_col] == '_':
                                    jump_row, jump_col = row + dr//2, col + dc//2
                                    jumped_piece = self.board.layout[jump_row, jump_col]
                                    if (self.current_player == Player.RED.value and jumped_piece in ['b', 'B']) or \
                                       (self.current_player == Player.BLACK.value and jumped_piece in ['r', 'R']):
                                        return True
        return False
        
    def perform_move(self, move):
        if is_movement(move):
            (from_pos, to_pos) = get_move_elements(move)
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            piece = self.board.layout[from_row, from_col]
            self.board.move_piece(move)
            
            # Check for capture
            if abs(from_row - to_row) == 2:
                jump_row = (from_row + to_row) // 2
                jump_col = (from_col + to_col) // 2
                jumped_piece = self.board.layout[jump_row, jump_col]
                
                # Special rule: if king captures king, both are removed
                if piece in ['R', 'B'] and jumped_piece in ['R', 'B']:
                    # Remove both kings
                    self.board.layout[jump_row, jump_col] = '_'
                    self.board.layout[to_row, to_col] = '_'
                else:
                    # Regular capture
                    self.board.layout[jump_row, jump_col] = '_'
                    
                # Check for additional captures
                if self.has_available_captures_from(to_row, to_col):
                    self.capture_chain = (to_row, to_col)
                else:
                    self.capture_chain = None
            else:
                self.capture_chain = None
                
            # Check for promotion to king
            if piece == 'r' and to_row == 0:
                self.board.layout[to_row, to_col] = 'R'
            elif piece == 'b' and to_row == self.board.height - 1:
                self.board.layout[to_row, to_col] = 'B'
                
    def has_available_captures_from(self, row, col):
        piece = self.board.layout[row, col]
        for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            if piece in ['r', 'R'] or (piece == 'r' and dr == -2) or (piece == 'b' and dr == 2):
                to_row, to_col = row + dr, col + dc
                if 0 <= to_row < self.board.height and 0 <= to_col < self.board.width:
                    if self.board.layout[to_row, to_col] == '_':
                        jump_row, jump_col = row + dr//2, col + dc//2
                        jumped_piece = self.board.layout[jump_row, jump_col]
                        if (self.current_player == Player.RED.value and jumped_piece in ['b', 'B']) or \
                           (self.current_player == Player.BLACK.value and jumped_piece in ['r', 'R']):
                            return True
        return False
        
    def prompt_current_player(self):
        player_name = "Red" if self.current_player == Player.RED.value else "Black"
        if self.capture_chain:
            return input(f"Player {player_name} (additional capture): ")
        return input(f"Player {player_name}: ")
        
    def next_player(self):
        if self.capture_chain:
            return self.current_player
        return Player.BLACK.value if self.current_player == Player.RED.value else Player.RED.value
        
    def game_finished(self):
        # Check if either player has no pieces left
        red_pieces = np.isin(self.board.layout, ['r', 'R']).sum()
        black_pieces = np.isin(self.board.layout, ['b', 'B']).sum()
        return red_pieces == 0 or black_pieces == 0
        
    def get_winner(self):
        red_pieces = np.isin(self.board.layout, ['r', 'R']).sum()
        black_pieces = np.isin(self.board.layout, ['b', 'B']).sum()
        
        if red_pieces == 0:
            return Player.BLACK.value
        elif black_pieces == 0:
            return Player.RED.value
        return None
        
    def get_state(self):
        state = super().get_state()
        additional_params = [self.capture_chain]
        return (state[0], state[1], additional_params)

if __name__ == '__main__':
    # Create initial board layout for checkers
    layout = """
 b _ b _ b _ b _
_ b _ b _ b _ b
 b _ b _ b _ b _
_ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _
_ r _ r _ r _ r
 r _ r _ r _ r _
_ r _ r _ r _ r
"""
    board = Board((8, 8), layout.strip())
    mygame = Checkers(board)
    mygame.game_loop()