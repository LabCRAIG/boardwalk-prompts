from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from enum import Enum

class Player(Enum):
    ONE = 1  # lowercase player
    TWO = 2  # uppercase player

class Obsidian(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.current_player = Player.ONE
        # Track whether pieces have moved (for pawn double move rule)
        self.moved_pieces = set()
        
    def initial_player(self):
        return Player.ONE
        
    def validate_move(self, move):
        # First check if the move is valid according to board bounds
        if not super().validate_move(move):
            return False
            
        # This game only allows movement, not placement
        if not is_movement(move):
            return False
            
        origin, destination = get_move_elements(move)
        o_row, o_col = origin
        d_row, d_col = destination
        
        # Get the piece being moved
        piece = self.board.layout[o_row][o_col]
        
        # Check if the piece belongs to current player
        if self.current_player == Player.ONE and not piece.islower():
            return False
        if self.current_player == Player.TWO and not piece.isupper():
            return False
            
        # Check if the destination is valid
        dest_piece = self.board.layout[d_row][d_col]
        if dest_piece != '_':  # If not blank
            # Can't capture own pieces
            if self.current_player == Player.ONE and dest_piece.islower():
                return False
            if self.current_player == Player.TWO and dest_piece.isupper():
                return False
        
        # Piece-specific movement validation
        piece_lower = piece.lower()
        
        if piece_lower == 'f':  # Pawn
            return self._validate_pawn_move(piece, origin, destination)
        elif piece_lower == 'a':  # Rook
            return self._validate_rook_move(piece, origin, destination)
        elif piece_lower == 'c':  # Bishop
            return self._validate_bishop_move(piece, origin, destination)
        elif piece_lower == 'b':  # Knight
            return self._validate_knight_move(piece, origin, destination)
        elif piece_lower == 'e':  # Queen
            return self._validate_queen_move(piece, origin, destination)
        elif piece_lower == 'd':  # King
            return self._validate_king_move(piece, origin, destination)
            
        return False
        
    def _validate_pawn_move(self, piece, origin, destination):
        o_row, o_col = origin
        d_row, d_col = destination
        
        # Direction depends on piece case
        direction = 1 if piece.isupper() else -1
        
        # Normal forward move (1 space)
        if o_col == d_col and d_row == o_row + direction:
            # Can only move forward to an empty space
            return self.board.layout[d_row][d_col] == '_'
        
        # Double move for first move
        has_moved = (o_row, o_col, piece) in self.moved_pieces
        if not has_moved and o_col == d_col and d_row == o_row + 2 * direction:
            # Ensure path is clear
            middle_row = o_row + direction
            return (self.board.layout[middle_row][o_col] == '_' and 
                    self.board.layout[d_row][d_col] == '_')
        
        # Diagonal capture
        if abs(o_col - d_col) == 1 and d_row == o_row + direction:
            dest_piece = self.board.layout[d_row][d_col]
            # Can only move diagonally if capturing
            if dest_piece != '_':  # If not blank
                # Check if it's an opponent's piece
                return ((piece.islower() and dest_piece.isupper()) or 
                        (piece.isupper() and dest_piece.islower()))
                        
        return False
        
    def _validate_rook_move(self, piece, origin, destination):
        o_row, o_col = origin
        d_row, d_col = destination
        
        # Must move orthogonally
        if o_row != d_row and o_col != d_col:
            return False
            
        # Check if path is clear
        if o_row == d_row:  # Horizontal move
            step = 1 if d_col > o_col else -1
            for col in range(o_col + step, d_col, step):
                if self.board.layout[o_row][col] != '_':
                    return False
        else:  # Vertical move
            step = 1 if d_row > o_row else -1
            for row in range(o_row + step, d_row, step):
                if self.board.layout[row][o_col] != '_':
                    return False
                    
        return True
        
    def _validate_bishop_move(self, piece, origin, destination):
        o_row, o_col = origin
        d_row, d_col = destination
        
        # Must move diagonally
        if abs(o_row - d_row) != abs(o_col - d_col):
            return False
            
        # Check if path is clear
        row_step = 1 if d_row > o_row else -1
        col_step = 1 if d_col > o_col else -1
        
        row, col = o_row + row_step, o_col + col_step
        while (row, col) != (d_row, d_col):
            if self.board.layout[row][col] != '_':
                return False
            row += row_step
            col += col_step
            
        return True
        
    def _validate_knight_move(self, piece, origin, destination):
        o_row, o_col = origin
        d_row, d_col = destination
        
        # Knight-like move (L shape)
        row_diff = abs(d_row - o_row)
        col_diff = abs(d_col - o_col)
        
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
        
    def _validate_queen_move(self, piece, origin, destination):
        # Queen moves like a rook or a bishop
        return (self._validate_rook_move(piece, origin, destination) or 
                self._validate_bishop_move(piece, origin, destination))
                
    def _validate_king_move(self, piece, origin, destination):
        o_row, o_col = origin
        d_row, d_col = destination
        
        # Can move one space in any direction
        return max(abs(o_row - d_row), abs(o_col - d_col)) == 1
        
    def perform_move(self, move):
        # Get move elements before modifying the board
        origin, destination = get_move_elements(move)
        o_row, o_col = origin
        d_row, d_col = destination
        piece = self.board.layout[o_row][o_col]
        
        # Track that this piece has moved
        self.moved_pieces.add((o_row, o_col, piece))
        
        # Standard move
        super().perform_move(move)
        
        # Check for pawn promotion
        if piece.lower() == 'f':
            # Check if pawn reached the promotion rank
            if (piece == 'f' and d_row == 0) or (piece == 'F' and d_row == 7):
                promoted_piece = 'e' if piece == 'f' else 'E'
                promotion_move = f"{promoted_piece} {d_row},{d_col}"
                self.board.place_piece(promotion_move)
        
    def game_finished(self):
        # Check if either king (D or d) has been captured
        has_uppercase_king = False
        has_lowercase_king = False
        
        for row in self.board.layout:
            for cell in row:
                if cell == 'D':
                    has_uppercase_king = True
                elif cell == 'd':
                    has_lowercase_king = True
                    
        return not (has_uppercase_king and has_lowercase_king)
    
    def get_winner(self):
        # If game is finished, determine winner
        if not self.game_finished():
            return None
            
        # Check which king is missing
        has_uppercase_king = False
        has_lowercase_king = False
        
        for row in self.board.layout:
            for cell in row:
                if cell == 'D':
                    has_uppercase_king = True
                elif cell == 'd':
                    has_lowercase_king = True
        
        if has_lowercase_king and not has_uppercase_king:
            return Player.ONE
        elif has_uppercase_king and not has_lowercase_king:
            return Player.TWO
        else:
            return None  # Draw (shouldn't happen in this game)
    
    def next_player(self):
        if self.current_player == Player.ONE:
            return Player.TWO
        else:
            return Player.ONE
            
    def finish_message(self, winner):
        if winner == Player.ONE:
            print("Player 1 (lowercase) wins!")
        else:
            print("Player 2 (uppercase) wins!")

if __name__ == '__main__':
    # Initialize board with the starting position for Obsidian
    initial_layout = """ABCDECBA
FFFFFFFF
________
________
________
________
ffffffff
abcdecba"""
    
    board = Board((8, 8), initial_layout)
    game = Obsidian(board)
    game.game_loop()