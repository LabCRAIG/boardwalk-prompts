from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from enum import Enum

class Player(Enum):
    WHITE = 0
    BLACK = 1

class Chess(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = self.initial_player()
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        
    def initial_player(self):
        return Player.WHITE.value
        
    def prompt_current_player(self):
        player_name = "White" if self.current_player == Player.WHITE.value else "Black"
        return input(f"Player {player_name}, enter your move: ")
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        try:
            if is_placement(move):
                piece, (row, col) = get_move_elements(move)
                if not self.is_valid_placement(piece, row, col):
                    return False
            elif is_movement(move):
                (from_row, from_col), (to_row, to_col) = get_move_elements(move)
                if not self.is_valid_movement(from_row, from_col, to_row, to_col):
                    return False
            else:
                return False
        except:
            return False
            
        return True
        
    def is_valid_placement(self, piece, row, col):
        # Only allow placements for pawn promotions
        if self.board.layout[row, col] != '_':
            return False
            
        current_color = 'white' if self.current_player == Player.WHITE.value else 'black'
        piece_color = 'white' if piece.isupper() else 'black'
        
        if piece_color != current_color:
            return False
            
        # Check if this is a pawn promotion scenario
        if row not in [0, 7]:  # Only allow promotions on first or last rank
            return False
            
        # Check if there's a pawn that can be promoted
        if current_color == 'white' and row == 7:
            pawn_row, pawn_col = 6, col
            if self.board.layout[pawn_row, pawn_col] != 'P':
                return False
        elif current_color == 'black' and row == 0:
            pawn_row, pawn_col = 1, col
            if self.board.layout[pawn_row, pawn_col] != 'p':
                return False
        else:
            return False
            
        return piece.upper() in ['Q', 'R', 'B', 'N']
        
    def is_valid_movement(self, from_row, from_col, to_row, to_col):
        piece = self.board.layout[from_row, from_col]
        if piece == '_' or piece == ' ':
            return False
            
        # Check if piece belongs to current player
        current_color = 'white' if self.current_player == Player.WHITE.value else 'black'
        piece_color = 'white' if piece.isupper() else 'black'
        if piece_color != current_color:
            return False
            
        # Check destination (can't capture own pieces)
        target = self.board.layout[to_row, to_col]
        if target != '_' and target != ' ':
            target_color = 'white' if target.isupper() else 'black'
            if target_color == current_color:
                return False
                
        # Piece-specific movement rules
        piece_type = piece.upper()
        
        if piece_type == 'P':
            return self.is_valid_pawn_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'R':
            return self.is_valid_rook_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'N':
            return self.is_valid_knight_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'B':
            return self.is_valid_bishop_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'Q':
            return self.is_valid_queen_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'K':
            return self.is_valid_king_move(from_row, from_col, to_row, to_col)
            
        return False
        
    def is_valid_pawn_move(self, from_row, from_col, to_row, to_col):
        direction = -1 if self.current_player == Player.WHITE.value else 1
        start_row = 6 if self.current_player == Player.WHITE.value else 1
        
        # Forward move
        if from_col == to_col:
            if to_row == from_row + direction and self.board.layout[to_row, to_col] == '_':
                return True
            # Double move from starting position
            if (from_row == start_row and to_row == from_row + 2*direction and 
                self.board.layout[from_row + direction, from_col] == '_' and 
                self.board.layout[to_row, to_col] == '_'):
                return True
                
        # Capture
        elif abs(from_col - to_col) == 1 and to_row == from_row + direction:
            target = self.board.layout[to_row, to_col]
            if target != '_' and target != ' ':
                target_color = 'white' if target.isupper() else 'black'
                current_color = 'white' if self.current_player == Player.WHITE.value else 'black'
                if target_color != current_color:
                    return True
                    
        # En passant (simplified)
        return False
        
    def is_valid_rook_move(self, from_row, from_col, to_row, to_col):
        if from_row != to_row and from_col != to_col:
            return False
            
        return self.is_path_clear(from_row, from_col, to_row, to_col)
        
    def is_valid_knight_move(self, from_row, from_col, to_row, to_col):
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
        
    def is_valid_bishop_move(self, from_row, from_col, to_row, to_col):
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
            
        return self.is_path_clear(from_row, from_col, to_row, to_col)
        
    def is_valid_queen_move(self, from_row, from_col, to_row, to_col):
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        
        if from_row == to_row or from_col == to_col or row_diff == col_diff:
            return self.is_path_clear(from_row, from_col, to_row, to_col)
            
        return False
        
    def is_valid_king_move(self, from_row, from_col, to_row, to_col):
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        return row_diff <= 1 and col_diff <= 1
        
    def is_path_clear(self, from_row, from_col, to_row, to_col):
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        current_row, current_col = from_row + row_step, from_col + col_step
        
        while current_row != to_row or current_col != to_col:
            if self.board.layout[current_row, current_col] != '_':
                return False
            current_row += row_step
            current_col += col_step
            
        return True
        
    def perform_move(self, move):
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
            # Remove the promoted pawn
            if self.current_player == Player.WHITE.value:
                self.board.layout[6, col] = '_'
            else:
                self.board.layout[1, col] = '_'
        else:
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            self.board.move_piece(move)
            
        # Update game state
        self.halfmove_clock += 1
        if self.current_player == Player.BLACK.value:
            self.fullmove_number += 1
            
    def game_finished(self):
        # Simplified: game ends when a king is captured
        white_king = False
        black_king = False
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                if piece == 'K':
                    white_king = True
                elif piece == 'k':
                    black_king = True
                    
        return not white_king or not black_king
        
    def get_winner(self):
        white_king = False
        black_king = False
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                if piece == 'K':
                    white_king = True
                elif piece == 'k':
                    black_king = True
                    
        if not white_king:
            return Player.BLACK.value
        elif not black_king:
            return Player.WHITE.value
        return None
        
    def next_player(self):
        return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value
        
    def finish_message(self, winner):
        if winner is None:
            print("The game ended in a draw!")
        else:
            winner_name = "White" if winner == Player.WHITE.value else "Black"
            print(f"Player {winner_name} wins!")

if __name__ == '__main__':
    # Create custom initial layout with knights in center (Reversi style)
    layout_str = """
r _ b q k b _ r
p p p p p p p p
_ _ _ _ _ _ _ _
_ _ _ N n _ _ _
_ _ _ n N _ _ _
_ _ _ _ _ _ _ _
P P P P P P P P
R _ B Q K B _ R
"""
    # Clean up the layout string
    layout_lines = [line.strip() for line in layout_str.strip().split('\n')]
    layout_str_clean = '\n'.join(layout_lines)
    
    board = Board((8, 8), layout_str_clean)
    mygame = Chess(board)
    mygame.game_loop()