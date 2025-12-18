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
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_kingside_moved = False
        self.white_rook_queenside_moved = False
        self.black_rook_kingside_moved = False
        self.black_rook_queenside_moved = False
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        
    def initial_player(self):
        return Player.WHITE.value
        
    def prompt_current_player(self):
        player_name = "White" if self.current_player == Player.WHITE.value else "Black"
        return input(f"Player {player_name}'s move: ")
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        try:
            if is_placement(move):
                piece, (row, col) = get_move_elements(move)
                return self._validate_placement(piece, row, col)
            elif is_movement(move):
                (from_row, from_col), (to_row, to_col) = get_move_elements(move)
                return self._validate_movement(from_row, from_col, to_row, to_col)
            else:
                # Check for special actions: bishop conversion or queen-rook swap
                parts = move.split()
                if len(parts) == 3 and parts[0] == "convert":
                    bishop_row, bishop_col = map(int, parts[1].split(','))
                    pawn_row, pawn_col = map(int, parts[2].split(','))
                    return self._validate_bishop_conversion(bishop_row, bishop_col, pawn_row, pawn_col)
                elif len(parts) == 3 and parts[0] == "swap":
                    queen_row, queen_col = map(int, parts[1].split(','))
                    rook_row, rook_col = map(int, parts[2].split(','))
                    return self._validate_queen_swap(queen_row, queen_col, rook_row, rook_col)
                return False
        except:
            return False
            
    def _validate_placement(self, piece, row, col):
        # Not used in standard chess
        return False
        
    def _validate_movement(self, from_row, from_col, to_row, to_col):
        if not (0 <= from_row < self.board.height and 0 <= from_col < self.board.width and
                0 <= to_row < self.board.height and 0 <= to_col < self.board.width):
            return False
            
        piece = self.board.layout[from_row, from_col]
        target = self.board.layout[to_row, to_col]
        
        # Check if piece belongs to current player
        if (self.current_player == Player.WHITE.value and not piece.isupper()) or \
           (self.current_player == Player.BLACK.value and piece.isupper()):
            return False
            
        # Check if target is not own piece
        if target != '_' and ((self.current_player == Player.WHITE.value and target.isupper()) or \
           (self.current_player == Player.BLACK.value and not target.isupper())):
            return False
            
        # Piece-specific movement validation
        piece_type = piece.upper()
        if piece_type == 'P':
            return self._validate_pawn_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'R':
            return self._validate_rook_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'N':
            return self._validate_knight_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'B':
            return self._validate_bishop_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'Q':
            return self._validate_queen_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'K':
            return self._validate_king_move(from_row, from_col, to_row, to_col)
        return False
        
    def _validate_pawn_move(self, from_row, from_col, to_row, to_col):
        direction = -1 if self.current_player == Player.WHITE.value else 1
        start_row = 6 if self.current_player == Player.WHITE.value else 1
        
        # Forward move
        if from_col == to_col:
            # Single step
            if to_row == from_row + direction and self.board.layout[to_row, to_col] == '_':
                return True
            # Double step from starting position
            if from_row == start_row and to_row == from_row + 2*direction and \
               self.board.layout[from_row + direction, from_col] == '_' and \
               self.board.layout[to_row, to_col] == '_':
                return True
            return False
            
        # Capture (diagonal)
        if abs(from_col - to_col) == 1 and to_row == from_row + direction:
            target = self.board.layout[to_row, to_col]
            if target != '_':
                # Normal capture
                if (self.current_player == Player.WHITE.value and target.islower()) or \
                   (self.current_player == Player.BLACK.value and target.isupper()):
                    return True
            # En passant
            if self.en_passant_target == (to_row, to_col):
                return True
        return False
        
    def _validate_rook_move(self, from_row, from_col, to_row, to_col):
        if from_row != to_row and from_col != to_col:
            return False
        return self._is_path_clear(from_row, from_col, to_row, to_col)
        
    def _validate_knight_move(self, from_row, from_col, to_row, to_col):
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
        
    def _validate_bishop_move(self, from_row, from_col, to_row, to_col):
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
        return self._is_path_clear(from_row, from_col, to_row, to_col)
        
    def _validate_queen_move(self, from_row, from_col, to_row, to_col):
        return self._validate_rook_move(from_row, from_col, to_row, to_col) or \
               self._validate_bishop_move(from_row, from_col, to_row, to_col)
        
    def _validate_king_move(self, from_row, from_col, to_row, to_col):
        # Normal king move
        if abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1:
            return True
            
        # Castling
        if from_row == to_row and abs(from_col - to_col) == 2:
            return self._validate_castling(from_row, from_col, to_row, to_col)
        return False
        
    def _validate_castling(self, from_row, from_col, to_row, to_col):
        if self.current_player == Player.WHITE.value:
            if self.white_king_moved:
                return False
            if to_col > from_col:  # Kingside
                if self.white_rook_kingside_moved:
                    return False
                if not self._is_path_clear(from_row, from_col, from_row, 7):
                    return False
                # Check if king passes through check
                for col in range(from_col, from_col + 3):
                    if self._is_square_under_attack(from_row, col, Player.BLACK.value):
                        return False
            else:  # Queenside
                if self.white_rook_queenside_moved:
                    return False
                if not self._is_path_clear(from_row, from_col, from_row, 0):
                    return False
                for col in range(from_col - 2, from_col + 1):
                    if self._is_square_under_attack(from_row, col, Player.BLACK.value):
                        return False
        else:
            if self.black_king_moved:
                return False
            if to_col > from_col:  # Kingside
                if self.black_rook_kingside_moved:
                    return False
                if not self._is_path_clear(from_row, from_col, from_row, 7):
                    return False
                for col in range(from_col, from_col + 3):
                    if self._is_square_under_attack(from_row, col, Player.WHITE.value):
                        return False
            else:  # Queenside
                if self.black_rook_queenside_moved:
                    return False
                if not self._is_path_clear(from_row, from_col, from_row, 0):
                    return False
                for col in range(from_col - 2, from_col + 1):
                    if self._is_square_under_attack(from_row, col, Player.WHITE.value):
                        return False
        return True
        
    def _is_path_clear(self, from_row, from_col, to_row, to_col):
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        current_row, current_col = from_row + row_step, from_col + col_step
        while current_row != to_row or current_col != to_col:
            if self.board.layout[current_row, current_col] != '_':
                return False
            current_row += row_step
            current_col += col_step
        return True
        
    def _is_square_under_attack(self, row, col, by_player):
        # Check for pawn attacks
        pawn_dir = -1 if by_player == Player.WHITE.value else 1
        for c_offset in [-1, 1]:
            attack_row, attack_col = row + pawn_dir, col + c_offset
            if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                piece = self.board.layout[attack_row, attack_col]
                if piece.upper() == 'P' and ((by_player == Player.WHITE.value and piece.isupper()) or \
                   (by_player == Player.BLACK.value and piece.islower())):
                    return True
        
        # Check for knight attacks
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = self.board.layout[r, c]
                if piece.upper() == 'N' and ((by_player == Player.WHITE.value and piece.isupper()) or \
                   (by_player == Player.BLACK.value and piece.islower())):
                    return True
        
        # Check for line attacks (rook, bishop, queen)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = self.board.layout[r, c]
                if piece != '_':
                    if (piece.upper() in ['R', 'Q'] and (dr == 0 or dc == 0)) or \
                       (piece.upper() in ['B', 'Q'] and (dr != 0 and dc != 0)):
                        if (by_player == Player.WHITE.value and piece.isupper()) or \
                           (by_player == Player.BLACK.value and piece.islower()):
                            return True
                    break
                r += dr
                c += dc
        
        # Check for king attacks
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    piece = self.board.layout[r, c]
                    if piece.upper() == 'K' and ((by_player == Player.WHITE.value and piece.isupper()) or \
                       (by_player == Player.BLACK.value and piece.islower())):
                        return True
        return False
        
    def _validate_bishop_conversion(self, bishop_row, bishop_col, pawn_row, pawn_col):
        # Check if bishop belongs to current player
        bishop = self.board.layout[bishop_row, bishop_col]
        if (self.current_player == Player.WHITE.value and not bishop.isupper()) or \
           (self.current_player == Player.BLACK.value and bishop.islower()):
            return False
            
        # Check if bishop is actually a bishop
        if bishop.upper() != 'B':
            return False
            
        # Check if target is a pawn of opposite color
        pawn = self.board.layout[pawn_row, pawn_col]
        if pawn.upper() != 'P':
            return False
        if (self.current_player == Player.WHITE.value and not pawn.islower()) or \
           (self.current_player == Player.BLACK.value and not pawn.isupper()):
            return False
            
        # Check if pawn is horizontally adjacent
        if abs(bishop_row - pawn_row) != 1 or abs(bishop_col - pawn_col) != 0:
            return False
            
        return True
        
    def _validate_queen_swap(self, queen_row, queen_col, rook_row, rook_col):
        # Check if queen belongs to current player
        queen = self.board.layout[queen_row, queen_col]
        if (self.current_player == Player.WHITE.value and not queen.isupper()) or \
           (self.current_player == Player.BLACK.value and queen.islower()):
            return False
            
        # Check if queen is actually a queen
        if queen.upper() != 'Q':
            return False
            
        # Check if rook belongs to current player
        rook = self.board.layout[rook_row, rook_col]
        if (self.current_player == Player.WHITE.value and not rook.isupper()) or \
           (self.current_player == Player.BLACK.value and rook.islower()):
            return False
            
        # Check if rook is actually a rook
        if rook.upper() != 'R':
            return False
            
        # Check if both pieces are on the same color square
        queen_color = (queen_row + queen_col) % 2
        rook_color = (rook_row + rook_col) % 2
        if queen_color != rook_color:
            return False
            
        return True
        
    def perform_move(self, move):
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            self.board.place_piece(move)
        elif is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            piece = self.board.layout[from_row, from_col]
            
            # Handle special moves
            if piece.upper() == 'K':
                self._handle_king_move(from_row, from_col, to_row, to_col)
            elif piece.upper() == 'R':
                self._handle_rook_move(from_row, from_col)
            elif piece.upper() == 'P':
                self._handle_pawn_move(from_row, from_col, to_row, to_col)
                
            self.board.move_piece(move)
            
            # Handle promotion
            if piece.upper() == 'P' and (to_row == 0 or to_row == 7):
                promo_piece = 'Q' if self.current_player == Player.WHITE.value else 'q'
                self.board.place_piece(f"{promo_piece} {to_row},{to_col}")
        else:
            parts = move.split()
            if len(parts) == 3 and parts[0] == "convert":
                bishop_row, bishop_col = map(int, parts[1].split(','))
                pawn_row, pawn_col = map(int, parts[2].split(','))
                self._perform_bishop_conversion(bishop_row, bishop_col, pawn_row, pawn_col)
            elif len(parts) == 3 and parts[0] == "swap":
                queen_row, queen_col = map(int, parts[1].split(','))
                rook_row, rook_col = map(int, parts[2].split(','))
                self._perform_queen_swap(queen_row, queen_col, rook_row, rook_col)
                
        # Update game state
        self.halfmove_clock += 1
        if self.current_player == Player.BLACK.value:
            self.fullmove_number += 1
            
    def _handle_king_move(self, from_row, from_col, to_row, to_col):
        if self.current_player == Player.WHITE.value:
            self.white_king_moved = True
            # Castling
            if abs(from_col - to_col) == 2:
                if to_col > from_col:  # Kingside
                    self.board.move_piece(f"{from_row},7 {from_row},{from_col+1}")
                else:  # Queenside
                    self.board.move_piece(f"{from_row},0 {from_row},{from_col-1}")
        else:
            self.black_king_moved = True
            if abs(from_col - to_col) == 2:
                if to_col > from_col:  # Kingside
                    self.board.move_piece(f"{from_row},7 {from_row},{from_col+1}")
                else:  # Queenside
                    self.board.move_piece(f"{from_row},0 {from_row},{from_col-1}")
                    
    def _handle_rook_move(self, from_row, from_col):
        if self.current_player == Player.WHITE.value:
            if from_row == 7:
                if from_col == 0:
                    self.white_rook_queenside_moved = True
                elif from_col == 7:
                    self.white_rook_kingside_moved = True
        else:
            if from_row == 0:
                if from_col == 0:
                    self.black_rook_queenside_moved = True
                elif from_col == 7:
                    self.black_rook_kingside_moved = True
                    
    def _handle_pawn_move(self, from_row, from_col, to_row, to_col):
        # Set en passant target
        if abs(from_row - to_row) == 2:
            self.en_passant_target = (from_row + (to_row - from_row) // 2, from_col)
        else:
            self.en_passant_target = None
            
        # Handle en passant capture
        if from_col != to_col and self.board.layout[to_row, to_col] == '_':
            # Remove the captured pawn
            capture_row = from_row
            capture_col = to_col
            self.board.place_piece(f"_ {capture_row},{capture_col}")
            
        # Reset halfmove clock for pawn moves and captures
        self.halfmove_clock = 0
        
    def _perform_bishop_conversion(self, bishop_row, bishop_col, pawn_row, pawn_col):
        # Convert the pawn to the bishop's color
        new_pawn = 'P' if self.current_player == Player.WHITE.value else 'p'
        self.board.place_piece(f"{new_pawn} {pawn_row},{pawn_col}")
        
    def _perform_queen_swap(self, queen_row, queen_col, rook_row, rook_col):
        # Swap queen and rook positions
        queen = self.board.layout[queen_row, queen_col]
        rook = self.board.layout[rook_row, rook_col]
        self.board.place_piece(f"{rook} {queen_row},{queen_col}")
        self.board.place_piece(f"{queen} {rook_row},{rook_col}")
        
    def game_finished(self):
        # Check for checkmate or stalemate
        king_symbol = 'K' if self.current_player == Player.WHITE.value else 'k'
        king_pos = None
        
        # Find the king
        for row in range(8):
            for col in range(8):
                if self.board.layout[row, col] == king_symbol:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
                
        if not king_pos:
            return True
            
        # Check if king is in check
        in_check = self._is_square_under_attack(king_pos[0], king_pos[1], 
                                               Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value)
        
        # Check for any legal moves
        has_legal_moves = False
        for from_row in range(8):
            for from_col in range(8):
                piece = self.board.layout[from_row, from_col]
                if (self.current_player == Player.WHITE.value and piece.isupper()) or \
                   (self.current_player == Player.BLACK.value and piece.islower()):
                    for to_row in range(8):
                        for to_col in range(8):
                            if self._validate_movement(from_row, from_col, to_row, to_col):
                                has_legal_moves = True
                                break
                        if has_legal_moves:
                            break
                    if has_legal_moves:
                        break
            if has_legal_moves:
                break
                
        # Also check for special actions
        if not has_legal_moves:
            # Check for bishop conversions
            for row in range(8):
                for col in range(8):
                    piece = self.board.layout[row, col]
                    if piece.upper() == 'B' and ((self.current_player == Player.WHITE.value and piece.isupper()) or \
                       (self.current_player == Player.BLACK.value and piece.islower())):
                        for dr in [-1, 1]:
                            pawn_row, pawn_col = row + dr, col
                            if 0 <= pawn_row < 8 and 0 <= pawn_col < 8:
                                pawn = self.board.layout[pawn_row, pawn_col]
                                if pawn.upper() == 'P' and ((self.current_player == Player.WHITE.value and pawn.islower()) or \
                                   (self.current_player == Player.BLACK.value and pawn.isupper())):
                                    has_legal_moves = True
                                    break
                        if has_legal_moves:
                            break
                if has_legal_moves:
                    break
                    
            # Check for queen swaps
            if not has_legal_moves:
                for q_row in range(8):
                    for q_col in range(8):
                        queen = self.board.layout[q_row, q_col]
                        if queen.upper() == 'Q' and ((self.current_player == Player.WHITE.value and queen.isupper()) or \
                           (self.current_player == Player.BLACK.value and queen.islower())):
                            queen_color = (q_row + q_col) % 2
                            for r_row in range(8):
                                for r_col in range(8):
                                    rook = self.board.layout[r_row, r_col]
                                    if rook.upper() == 'R' and ((self.current_player == Player.WHITE.value and rook.isupper()) or \
                                       (self.current_player == Player.BLACK.value and rook.islower())):
                                        rook_color = (r_row + r_col) % 2
                                        if queen_color == rook_color:
                                            has_legal_moves = True
                                            break
                                if has_legal_moves:
                                    break
                            if has_legal_moves:
                                break
                    if has_legal_moves:
                        break
                        
        if not has_legal_moves:
            return True
            
        # Check for 50-move rule
        if self.halfmove_clock >= 100:
            return True
            
        # Check for insufficient material
        return False
        
    def get_winner(self):
        # Check if current player is in checkmate
        king_symbol = 'K' if self.current_player == Player.WHITE.value else 'k'
        king_pos = None
        
        for row in range(8):
            for col in range(8):
                if self.board.layout[row, col] == king_symbol:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
                
        if not king_pos:
            return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value
            
        in_check = self._is_square_under_attack(king_pos[0], king_pos[1], 
                                               Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value)
        
        if in_check:
            return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value
            
        # Stalemate or draw
        return None
        
    def next_player(self):
        return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value
        
    def round_counter(self):
        return self.round + 1
        
    def finish_message(self, winner):
        if winner is None:
            print("The game ended in a draw!")
        else:
            winner_name = "White" if winner == Player.WHITE.value else "Black"
            print(f"Player {winner_name} wins!")

if __name__ == '__main__':
    # Standard chess starting position
    initial_layout = (
        "rnbqkbnr\n"
        "pppppppp\n"
        "________\n"
        "________\n"
        "________\n"
        "________\n"
        "PPPPPPPP\n"
        "RNBQKBNR"
    )
    board = Board((8, 8), initial_layout)
    chess_game = Chess(board)
    chess_game.game_loop()