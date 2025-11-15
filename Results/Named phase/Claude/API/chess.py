
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    WHITE = 0
    BLACK = 1

class Chess(Game):
    def __init__(self, board):
        super().__init__(board)
        self.castling_rights = {
            Player.WHITE: {'king_moved': False, 'rook_a_moved': False, 'rook_h_moved': False},
            Player.BLACK: {'king_moved': False, 'rook_a_moved': False, 'rook_h_moved': False}
        }
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
    
    def initial_player(self):
        return Player.WHITE.value
    
    def get_state(self):
        board_layout = deepcopy(self.board.layout)
        additional_params = [
            self.castling_rights,
            self.en_passant_target,
            self.halfmove_clock,
            self.fullmove_number,
            self.white_king_pos,
            self.black_king_pos
        ]
        return (board_layout, self.current_player, additional_params)
    
    def prompt_current_player(self):
        player_name = "White" if self.current_player == Player.WHITE.value else "Black"
        return input(f"{player_name}'s move: ")
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        # Check if move format is valid
        if not (is_movement(move) or is_placement(move)):
            return False
        
        # Movement validation
        if is_movement(move):
            origin, destination = get_move_elements(move)
            row_orig, col_orig = origin
            row_dest, col_dest = destination
            
            # Check if origin square has a piece owned by current player
            piece = self.board.layout[row_orig][col_orig]
            if piece == '_':
                return False
                
            # Check if piece belongs to current player
            if self.current_player == Player.WHITE.value and not piece.isupper():
                return False
            if self.current_player == Player.BLACK.value and not piece.islower():
                return False
                
            # Check if destination has opponent's piece or is empty
            dest_piece = self.board.layout[row_dest][col_dest]
            if dest_piece != '_':
                if self.current_player == Player.WHITE.value and dest_piece.isupper():
                    return False
                if self.current_player == Player.BLACK.value and dest_piece.islower():
                    return False
            
            # Validate piece-specific movement
            if piece.upper() == 'P':
                return self._validate_pawn_move(origin, destination)
            elif piece.upper() == 'R':
                return self._validate_rook_move(origin, destination)
            elif piece.upper() == 'N':
                return self._validate_knight_move(origin, destination)
            elif piece.upper() == 'B':
                return self._validate_bishop_move(origin, destination)
            elif piece.upper() == 'Q':
                return self._validate_queen_move(origin, destination)
            elif piece.upper() == 'K':
                return self._validate_king_move(origin, destination)
            else:
                return False
                
        # No placement moves in chess after initial setup
        return False
    
    def _validate_pawn_move(self, origin, destination):
        row_orig, col_orig = origin
        row_dest, col_dest = destination
        piece = self.board.layout[row_orig][col_orig]
        dest_piece = self.board.layout[row_dest][col_dest]
        
        # Direction depends on color
        direction = 1 if self.current_player == Player.BLACK.value else -1
        start_row = 1 if self.current_player == Player.BLACK.value else 6
        
        # Normal move - 1 square forward
        if col_orig == col_dest and row_dest == row_orig + direction and dest_piece == '_':
            return True
            
        # First move - 2 squares forward
        if col_orig == col_dest and row_orig == start_row and row_dest == row_orig + 2*direction:
            # Check if path is clear
            if self.board.layout[row_orig + direction][col_orig] == '_' and dest_piece == '_':
                return True
        
        # Capture - diagonal move
        if abs(col_dest - col_orig) == 1 and row_dest == row_orig + direction:
            # Regular capture
            if dest_piece != '_':
                return True
                
            # En passant capture
            if self.en_passant_target == (row_dest, col_dest):
                return True
                
        return False
    
    def _validate_rook_move(self, origin, destination):
        row_orig, col_orig = origin
        row_dest, col_dest = destination
        
        # Rook moves horizontally or vertically
        if row_orig != row_dest and col_orig != col_dest:
            return False
            
        # Check if path is clear
        return self._is_path_clear(origin, destination)
    
    def _validate_knight_move(self, origin, destination):
        row_orig, col_orig = origin
        row_dest, col_dest = destination
        
        # Knight moves in L-shape
        row_diff = abs(row_dest - row_orig)
        col_diff = abs(col_dest - col_orig)
        
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def _validate_bishop_move(self, origin, destination):
        row_orig, col_orig = origin
        row_dest, col_dest = destination
        
        # Bishop moves diagonally
        if abs(row_dest - row_orig) != abs(col_dest - col_orig):
            return False
            
        # Check if path is clear
        return self._is_path_clear(origin, destination)
    
    def _validate_queen_move(self, origin, destination):
        # Queen moves like rook or bishop
        return self._validate_rook_move(origin, destination) or self._validate_bishop_move(origin, destination)
    
    def _validate_king_move(self, origin, destination):
        row_orig, col_orig = origin
        row_dest, col_dest = destination
        
        # Normal king move - 1 square in any direction
        if abs(row_dest - row_orig) <= 1 and abs(col_dest - col_orig) <= 1:
            return True
            
        # Castling
        if row_orig == row_dest and abs(col_dest - col_orig) == 2:
            # Check if king and rook haven't moved
            if self.current_player == Player.WHITE.value:
                if self.castling_rights[Player.WHITE]['king_moved']:
                    return False
                    
                # Kingside castling
                if col_dest > col_orig and not self.castling_rights[Player.WHITE]['rook_h_moved']:
                    return self._is_path_clear(origin, (row_orig, 7)) and not self._is_king_in_check(Player.WHITE.value)
                    
                # Queenside castling
                if col_dest < col_orig and not self.castling_rights[Player.WHITE]['rook_a_moved']:
                    return self._is_path_clear(origin, (row_orig, 0)) and not self._is_king_in_check(Player.WHITE.value)
            else:
                if self.castling_rights[Player.BLACK]['king_moved']:
                    return False
                    
                # Kingside castling
                if col_dest > col_orig and not self.castling_rights[Player.BLACK]['rook_h_moved']:
                    return self._is_path_clear(origin, (row_orig, 7)) and not self._is_king_in_check(Player.BLACK.value)
                    
                # Queenside castling
                if col_dest < col_orig and not self.castling_rights[Player.BLACK]['rook_a_moved']:
                    return self._is_path_clear(origin, (row_orig, 0)) and not self._is_king_in_check(Player.BLACK.value)
                    
        return False
    
    def _is_path_clear(self, origin, destination):
        row_orig, col_orig = origin
        row_dest, col_dest = destination
        
        row_step = 0 if row_orig == row_dest else (1 if row_dest > row_orig else -1)
        col_step = 0 if col_orig == col_dest else (1 if col_dest > col_orig else -1)
        
        row, col = row_orig + row_step, col_orig + col_step
        
        while (row, col) != (row_dest, col_dest):
            if self.board.layout[row][col] != '_':
                return False
            row += row_step
            col += col_step
            
        return True
    
    def _is_king_in_check(self, player):
        # Find king position
        king_pos = self.white_king_pos if player == Player.WHITE.value else self.black_king_pos
        
        # Check if any opponent piece can capture the king
        opponent = Player.BLACK.value if player == Player.WHITE.value else Player.WHITE.value
        
        for row in range(8):
            for col in range(8):
                piece = self.board.layout[row][col]
                
                # Skip empty squares and player's own pieces
                if piece == '_':
                    continue
                    
                if (player == Player.WHITE.value and piece.isupper()) or (player == Player.BLACK.value and piece.islower()):
                    continue
                    
                # Check if this piece can move to the king's position
                origin = (row, col)
                
                if piece.upper() == 'P':
                    if self._validate_pawn_move(origin, king_pos):
                        return True
                elif piece.upper() == 'R':
                    if self._validate_rook_move(origin, king_pos):
                        return True
                elif piece.upper() == 'N':
                    if self._validate_knight_move(origin, king_pos):
                        return True
                elif piece.upper() == 'B':
                    if self._validate_bishop_move(origin, king_pos):
                        return True
                elif piece.upper() == 'Q':
                    if self._validate_queen_move(origin, king_pos):
                        return True
                elif piece.upper() == 'K':
                    # Kings can't check each other directly
                    row_diff = abs(king_pos[0] - row)
                    col_diff = abs(king_pos[1] - col)
                    if row_diff <= 1 and col_diff <= 1:
                        return True
                        
        return False
    
    def perform_move(self, move):
        if is_movement(move):
            origin, destination = get_move_elements(move)
            row_orig, col_orig = origin
            row_dest, col_dest = destination
            piece = self.board.layout[row_orig][col_orig]
            dest_piece = self.board.layout[row_dest][col_dest]
            
            # Update halfmove clock
            if piece.upper() == 'P' or dest_piece != '_':
                self.halfmove_clock = 0
            else:
                self.halfmove_clock += 1
                
            # Track king positions
            if piece.upper() == 'K':
                if self.current_player == Player.WHITE.value:
                    self.white_king_pos = destination
                else:
                    self.black_king_pos = destination
                    
                # Update castling rights
                if self.current_player == Player.WHITE.value:
                    self.castling_rights[Player.WHITE]['king_moved'] = True
                else:
                    self.castling_rights[Player.BLACK]['king_moved'] = True
                    
                # Handle castling
                if abs(col_dest - col_orig) == 2:
                    # Kingside castling
                    if col_dest > col_orig:
                        rook_orig = (row_orig, 7)
                        rook_dest = (row_orig, 5)
                        self.board.move_piece(f"{rook_orig[0]},{rook_orig[1]} {rook_dest[0]},{rook_dest[1]}")
                    # Queenside castling
                    else:
                        rook_orig = (row_orig, 0)
                        rook_dest = (row_orig, 3)
                        self.board.move_piece(f"{rook_orig[0]},{rook_orig[1]} {rook_dest[0]},{rook_dest[1]}")
            
            # Update rook castling rights
            if piece.upper() == 'R':
                if self.current_player == Player.WHITE.value:
                    if origin == (7, 0):
                        self.castling_rights[Player.WHITE]['rook_a_moved'] = True
                    elif origin == (7, 7):
                        self.castling_rights[Player.WHITE]['rook_h_moved'] = True
                else:
                    if origin == (0, 0):
                        self.castling_rights[Player.BLACK]['rook_a_moved'] = True
                    elif origin == (0, 7):
                        self.castling_rights[Player.BLACK]['rook_h_moved'] = True
                        
            # Handle en passant
            self.en_passant_target = None
            if piece.upper() == 'P':
                # Set en passant target if pawn moves 2 squares
                if abs(row_dest - row_orig) == 2:
                    self.en_passant_target = (row_orig + (row_dest - row_orig)//2, col_orig)
                    
                # Capture en passant
                if col_dest != col_orig and dest_piece == '_':
                    captured_pawn_row = row_orig
                    captured_pawn_col = col_dest
                    self.board.place_piece(f"_ {captured_pawn_row},{captured_pawn_col}")
                    
                # Pawn promotion
                if (row_dest == 0 and self.current_player == Player.WHITE.value) or (row_dest == 7 and self.current_player == Player.BLACK.value):
                    promotion_piece = 'Q' if self.current_player == Player.WHITE.value else 'q'
                    super().perform_move(move)
                    self.board.place_piece(f"{promotion_piece} {row_dest},{col_dest}")
                    return
                    
            super().perform_move(move)
            
            # Update fullmove number after Black's move
            if self.current_player == Player.BLACK.value:
                self.fullmove_number += 1
    
    def game_finished(self):
        # Check for checkmate or stalemate
        player = self.current_player
        
        # If king is in check and no legal moves, it's checkmate
        # If king is not in check and no legal moves, it's stalemate
        if self._is_king_in_check(player):
            if self._has_no_legal_moves(player):
                return True
        else:
            if self._has_no_legal_moves(player):
                return True
                
        # Draw by insufficient material
        if self._is_insufficient_material():
            return True
            
        # Draw by 50-move rule
        if self.halfmove_clock >= 50:
            return True
            
        return False
    
    def _has_no_legal_moves(self, player):
        # Check if any piece has a legal move
        for row_orig in range(8):
            for col_orig in range(8):
                piece = self.board.layout[row_orig][col_orig]
                
                # Skip empty squares and opponent's pieces
                if piece == '_':
                    continue
                    
                if (player == Player.WHITE.value and not piece.isupper()) or (player == Player.BLACK.value and not piece.islower()):
                    continue
                    
                # Try all possible destinations
                for row_dest in range(8):
                    for col_dest in range(8):
                        move = f"{row_orig},{col_orig} {row_dest},{col_dest}"
                        
                        if self.validate_move(move):
                            # Make the move temporarily to see if it leaves the king in check
                            temp_board = deepcopy(self.board.layout)
                            temp_king_pos = deepcopy(self.white_king_pos if player == Player.WHITE.value else self.black_king_pos)
                            
                            # Update king position if king is moved
                            if piece.upper() == 'K':
                                if player == Player.WHITE.value:
                                    self.white_king_pos = (row_dest, col_dest)
                                else:
                                    self.black_king_pos = (row_dest, col_dest)
                                    
                            # Make the move
                            self.board.move_piece(move)
                            
                            # Check if the king is in check
                            in_check = self._is_king_in_check(player)
                            
                            # Restore the board
                            self.board.layout = temp_board
                            if player == Player.WHITE.value:
                                self.white_king_pos = temp_king_pos
                            else:
                                self.black_king_pos = temp_king_pos
                                
                            if not in_check:
                                return False
        
        return True
    
    def _is_insufficient_material(self):
        # Count pieces
        white_pieces = []
        black_pieces = []
        
        for row in range(8):
            for col in range(8):
                piece = self.board.layout[row][col]
                if piece != '_':
                    if piece.isupper():
                        white_pieces.append(piece)
                    else:
                        black_pieces.append(piece)
        
        # King vs King
        if len(white_pieces) == 1 and len(black_pieces) == 1:
            return True
            
        # King + Knight/Bishop vs King
        if (len(white_pieces) == 2 and len(black_pieces) == 1 and 
            (any(p in white_pieces for p in ['N', 'B']))):
            return True
            
        if (len(black_pieces) == 2 and len(white_pieces) == 1 and 
            (any(p in [p.upper() for p in black_pieces] for p in ['N', 'B']))):
            return True
            
        # King + Bishop vs King + Bishop (same color)
        if len(white_pieces) == 2 and len(black_pieces) == 2:
            white_bishop = None
            black_bishop = None
            
            for p in white_pieces:
                if p == 'B':
                    white_bishop = p
                    
            for p in black_pieces:
                if p.upper() == 'B':
                    black_bishop = p
                    
            if white_bishop and black_bishop:
                # Check if bishops are on same color squares
                white_bishop_pos = None
                black_bishop_pos = None
                
                for row in range(8):
                    for col in range(8):
                        if self.board.layout[row][col] == 'B':
                            white_bishop_pos = (row, col)
                        elif self.board.layout[row][col] == 'b':
                            black_bishop_pos = (row, col)
                
                if white_bishop_pos and black_bishop_pos:
                    # Bishops on same color if (row+col) % 2 is same for both
                    if (white_bishop_pos[0] + white_bishop_pos[1]) % 2 == (black_bishop_pos[0] + black_bishop_pos[1]) % 2:
                        return True
        
        return False
    
    def get_winner(self):
        if not self.game_finished():
            return None
            
        # Check for checkmate
        if self._is_king_in_check(self.current_player) and self._has_no_legal_moves(self.current_player):
            return Player.WHITE.value if self.current_player == Player.BLACK.value else Player.BLACK.value
            
        # Draw conditions
        return None
    
    def next_player(self):
        return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value
    
    def finish_message(self, winner):
        if winner is not None:
            winner_name = "White" if winner == Player.WHITE.value else "Black"
            print(f"\n{winner_name} wins by checkmate!")
        else:
            print("\nGame drawn!")
            
            # Determine draw reason
            if self.halfmove_clock >= 50:
                print("Draw by fifty-move rule.")
            elif self._is_insufficient_material():
                print("Draw by insufficient material.")
            else:
                print("Draw by stalemate.")

if __name__ == '__main__':
    # Initial chess layout
    layout = (
        "rnbqkbnr\n"
        "pppppppp\n"
        "________\n"
        "________\n"
        "________\n"
        "________\n"
        "PPPPPPPP\n"
        "RNBQKBNR"
    )
    board = Board((8, 8), layout)
    chess = Chess(board)
    chess.game_loop()
