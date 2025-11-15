
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy
import re

class ChessPlayer(Enum):
    WHITE = 0
    BLACK = 1

class Chess(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = self.initial_player()
        # Track castling rights
        self.white_can_castle_kingside = True
        self.white_can_castle_queenside = True
        self.black_can_castle_kingside = True
        self.black_can_castle_queenside = True
        # Track king positions
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        # Track en passant target
        self.en_passant_target = None
        # Track halfmove clock (for 50-move rule)
        self.halfmove_clock = 0
        # Piece movement directions
        self.directions = {
            'N': [(-1, 0)],
            'B': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
            'R': [(0, 1), (1, 0), (0, -1), (-1, 0)],
            'Q': [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)],
            'K': [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        }

    def initial_player(self):
        return ChessPlayer.WHITE.value

    def next_player(self):
        return ChessPlayer.BLACK.value if self.current_player == ChessPlayer.WHITE.value else ChessPlayer.WHITE.value

    def prompt_current_player(self):
        player_name = "White" if self.current_player == ChessPlayer.WHITE.value else "Black"
        move = input(f"{player_name}'s move: ")

        # Handle special moves notation
        if move.lower() == "o-o" or move.lower() == "0-0":  # Kingside castling
            rank = 7 if self.current_player == ChessPlayer.WHITE.value else 0
            return f"{rank},4 {rank},6"
        elif move.lower() == "o-o-o" or move.lower() == "0-0-0":  # Queenside castling
            rank = 7 if self.current_player == ChessPlayer.WHITE.value else 0
            return f"{rank},4 {rank},2"

        # Convert algebraic notation to coordinate notation
        if re.match(r'^[a-h][1-8][a-h][1-8]$', move):  # Format like "e2e4"
            file_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
            from_file, from_rank, to_file, to_rank = move[0], move[1], move[2], move[3]
            from_col = file_map[from_file]
            from_row = 8 - int(from_rank)
            to_col = file_map[to_file]
            to_row = 8 - int(to_rank)
            return f"{from_row},{from_col} {to_row},{to_col}"

        return move

    def get_state(self):
        state = super().get_state()
        additional_state = [
            self.white_can_castle_kingside,
            self.white_can_castle_queenside,
            self.black_can_castle_kingside,
            self.black_can_castle_queenside,
            self.en_passant_target,
            self.halfmove_clock,
            self.white_king_pos,
            self.black_king_pos
        ]
        return (state[0], state[1], additional_state)

    def is_white_piece(self, piece):
        return piece in 'PNBRQK'

    def is_black_piece(self, piece):
        return piece in 'pnbrqk'

    def get_piece_color(self, piece):
        if self.is_white_piece(piece):
            return ChessPlayer.WHITE.value
        elif self.is_black_piece(piece):
            return ChessPlayer.BLACK.value
        return None

    def is_capture(self, dest_row, dest_col):
        dest_piece = self.board.layout[dest_row][dest_col]
        return dest_piece != '_'

    def is_en_passant_capture(self, from_row, from_col, to_row, to_col):
        if self.en_passant_target is None:
            return False

        piece = self.board.layout[from_row][from_col]
        en_passant_row, en_passant_col = self.en_passant_target

        return ((piece == 'P' or piece == 'p') and 
                to_row == en_passant_row and 
                to_col == en_passant_col)

    def is_pawn_promotion(self, from_row, from_col, to_row):
        piece = self.board.layout[from_row][from_col]
        return (piece == 'P' and to_row == 0) or (piece == 'p' and to_row == 7)

    def validate_move(self, move):
        if not super().validate_move(move):
            return False

        if not is_movement(move):
            return False

        (from_row, from_col), (to_row, to_col) = get_move_elements(move)
        
        # Check if there's a piece at the origin
        piece = self.board.layout[from_row][from_col]
        if piece == '_' or piece == ' ':
            return False
        
        # Check if player is moving their own piece
        piece_color = self.get_piece_color(piece)
        if piece_color != self.current_player:
            return False
            
        # Can't capture own piece
        dest_piece = self.board.layout[to_row][to_col]
        if dest_piece != '_' and self.get_piece_color(dest_piece) == piece_color:
            return False

        # Check piece-specific movement rules
        if not self.is_valid_piece_move(piece, from_row, from_col, to_row, to_col):
            return False
            
        # Simulate the move to check if it would leave the king in check
        original_layout = deepcopy(self.board.layout)
        
        # Track king position
        original_king_pos = self.white_king_pos if piece_color == ChessPlayer.WHITE.value else self.black_king_pos
        king_moved = False
        
        if piece.upper() == 'K':
            king_moved = True
            if piece_color == ChessPlayer.WHITE.value:
                self.white_king_pos = (to_row, to_col)
            else:
                self.black_king_pos = (to_row, to_col)
                
        # Perform move simulation
        self.board.layout[to_row][to_col] = piece
        self.board.layout[from_row][from_col] = '_'
        
        # Handle en passant capture in simulation
        if self.is_en_passant_capture(from_row, from_col, to_row, to_col):
            capture_row = from_row
            capture_col = to_col
            self.board.layout[capture_row][capture_col] = '_'
            
        # Check if king is in check after the move
        king_pos = self.white_king_pos if piece_color == ChessPlayer.WHITE.value else self.black_king_pos
        in_check = self.is_square_attacked(king_pos[0], king_pos[1], piece_color)
        
        # Restore the original board layout
        self.board.layout = original_layout
        
        # Restore king position if it was moved
        if king_moved:
            if piece_color == ChessPlayer.WHITE.value:
                self.white_king_pos = original_king_pos
            else:
                self.black_king_pos = original_king_pos
        
        return not in_check

    def is_valid_piece_move(self, piece, from_row, from_col, to_row, to_col):
        piece_type = piece.upper()
        
        # Check if the move is castling
        if piece_type == 'K' and abs(from_col - to_col) == 2:
            return self.is_valid_castling(from_row, from_col, to_row, to_col)
            
        # Pawn movement
        if piece_type == 'P':
            return self.is_valid_pawn_move(piece, from_row, from_col, to_row, to_col)
            
        # Knight movement
        if piece_type == 'N':
            knight_moves = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ]
            move = (to_row - from_row, to_col - from_col)
            return move in knight_moves
            
        # For sliding pieces (Bishop, Rook, Queen, King)
        if piece_type in self.directions:
            # King can only move one square (except castling, handled separately)
            if piece_type == 'K':
                if abs(to_row - from_row) > 1 or abs(to_col - from_col) > 1:
                    return False
                    
            # Check if the move is along a valid direction for the piece
            dr = to_row - from_row
            dc = to_col - from_col
            
            # Determine direction vector
            direction = None
            if dr != 0 and dc != 0:  # Diagonal
                if abs(dr) != abs(dc):  # Must be a perfect diagonal
                    return False
                direction = (dr // abs(dr), dc // abs(dc))
            elif dr != 0:  # Vertical
                direction = (dr // abs(dr), 0)
            elif dc != 0:  # Horizontal
                direction = (0, dc // abs(dc))
                
            if direction not in self.directions[piece_type]:
                return False
                
            # Check if the path is clear
            steps = max(abs(dr), abs(dc))
            for i in range(1, steps):
                r = from_row + direction[0] * i
                c = from_col + direction[1] * i
                if self.board.layout[r][c] != '_':
                    return False
                    
            return True
            
        return False

    def is_valid_pawn_move(self, piece, from_row, from_col, to_row, to_col):
        direction = -1 if piece == 'P' else 1  # White moves up (-1), Black moves down (1)
        
        # Forward movement (non-capture)
        if from_col == to_col:
            # Single square forward
            if to_row == from_row + direction and self.board.layout[to_row][to_col] == '_':
                return True
                
            # Double square forward from starting position
            start_row = 6 if piece == 'P' else 1
            if (from_row == start_row and 
                to_row == from_row + 2 * direction and 
                self.board.layout[from_row + direction][from_col] == '_' and 
                self.board.layout[to_row][to_col] == '_'):
                return True
                
            return False
            
        # Diagonal capture
        if abs(from_col - to_col) == 1 and to_row == from_row + direction:
            # Regular capture
            if self.board.layout[to_row][to_col] != '_' and self.get_piece_color(self.board.layout[to_row][to_col]) != self.get_piece_color(piece):
                return True
                
            # En passant capture
            if self.en_passant_target == (to_row, to_col):
                return True
                
        return False

    def is_valid_castling(self, from_row, from_col, to_row, to_col):
        # Must be on the correct rank
        if (self.current_player == ChessPlayer.WHITE.value and from_row != 7) or \
           (self.current_player == ChessPlayer.BLACK.value and from_row != 0):
            return False
            
        # Must be king's initial position
        if from_col != 4:
            return False
            
        # Must move horizontally to correct position
        if from_row != to_row or (to_col != 2 and to_col != 6):
            return False
            
        # Kingside castling
        if to_col == 6:
            if (self.current_player == ChessPlayer.WHITE.value and not self.white_can_castle_kingside) or \
               (self.current_player == ChessPlayer.BLACK.value and not self.black_can_castle_kingside):
                return False
                
            # Check if path is clear
            if self.board.layout[from_row][5] != '_' or self.board.layout[from_row][6] != '_':
                return False
                
            # Check if king or path is in check
            if (self.is_square_attacked(from_row, from_col, self.current_player) or
                self.is_square_attacked(from_row, 5, self.current_player) or
                self.is_square_attacked(from_row, 6, self.current_player)):
                return False
                
            return True
            
        # Queenside castling
        if to_col == 2:
            if (self.current_player == ChessPlayer.WHITE.value and not self.white_can_castle_queenside) or \
               (self.current_player == ChessPlayer.BLACK.value and not self.black_can_castle_queenside):
                return False
                
            # Check if path is clear
            if (self.board.layout[from_row][1] != '_' or 
                self.board.layout[from_row][2] != '_' or 
                self.board.layout[from_row][3] != '_'):
                return False
                
            # Check if king or path is in check
            if (self.is_square_attacked(from_row, from_col, self.current_player) or
                self.is_square_attacked(from_row, 3, self.current_player) or
                self.is_square_attacked(from_row, 2, self.current_player)):
                return False
                
            return True
            
        return False

    def is_square_attacked(self, row, col, defender_color):
        opponent_color = ChessPlayer.BLACK.value if defender_color == ChessPlayer.WHITE.value else ChessPlayer.WHITE.value
        
        # Check for pawn attacks
        pawn_direction = 1 if defender_color == ChessPlayer.WHITE.value else -1
        pawn_piece = 'p' if defender_color == ChessPlayer.WHITE.value else 'P'
        
        for col_offset in [-1, 1]:
            attack_row = row + pawn_direction
            attack_col = col + col_offset
            if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                if self.board.layout[attack_row][attack_col] == pawn_piece:
                    return True
        
        # Check for knight attacks
        knight_piece = 'n' if defender_color == ChessPlayer.WHITE.value else 'N'
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            attack_row = row + dr
            attack_col = col + dc
            if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                if self.board.layout[attack_row][attack_col] == knight_piece:
                    return True
        
        # Check for king attacks
        king_piece = 'k' if defender_color == ChessPlayer.WHITE.value else 'K'
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                attack_row = row + dr
                attack_col = col + dc
                if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                    if self.board.layout[attack_row][attack_col] == king_piece:
                        return True
        
        # Check for sliding piece attacks (queen, rook, bishop)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Rook/Queen directions
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Bishop/Queen directions
        ]
        
        for dr, dc in directions:
            for i in range(1, 8):
                attack_row = row + dr * i
                attack_col = col + dc * i
                
                if not (0 <= attack_row < 8 and 0 <= attack_col < 8):
                    break
                    
                piece = self.board.layout[attack_row][attack_col]
                if piece == '_':
                    continue
                    
                if self.get_piece_color(piece) == defender_color:
                    break
                    
                piece_type = piece.upper()
                if (piece_type == 'Q' or 
                    (piece_type == 'R' and dr * dc == 0) or  # Rook moves orthogonally
                    (piece_type == 'B' and dr * dc != 0)):   # Bishop moves diagonally
                    return True
                    
                break  # Blocked by an opponent's piece that can't attack in this direction
                
        return False

    def perform_move(self, move):
        (from_row, from_col), (to_row, to_col) = get_move_elements(move)
        piece = self.board.layout[from_row][from_col]
        dest_piece = self.board.layout[to_row][to_col]
        
        # Reset en passant target
        prev_en_passant = self.en_passant_target
        self.en_passant_target = None
        
        # Update halfmove clock
        if piece.upper() == 'P' or dest_piece != '_':
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
            
        # Handle pawn double move (set en passant target)
        if piece.upper() == 'P' and abs(from_row - to_row) == 2:
            self.en_passant_target = (from_row + (1 if from_row < to_row else -1), from_col)
            
        # Handle en passant capture
        if piece.upper() == 'P' and (to_row, to_col) == prev_en_passant:
            capture_row = from_row
            capture_col = to_col
            # Remove the captured pawn
            self.board.layout[capture_row][capture_col] = '_'
            
        # Handle castling
        if piece.upper() == 'K' and abs(from_col - to_col) == 2:
            rook_from_col = 7 if to_col > from_col else 0
            rook_to_col = 5 if to_col > from_col else 3
            
            # Move the rook
            rook = self.board.layout[from_row][rook_from_col]
            self.board.layout[from_row][rook_to_col] = rook
            self.board.layout[from_row][rook_from_col] = '_'
            
        # Update castling rights
        if piece.upper() == 'K':
            if self.current_player == ChessPlayer.WHITE.value:
                self.white_can_castle_kingside = False
                self.white_can_castle_queenside = False
                self.white_king_pos = (to_row, to_col)
            else:
                self.black_can_castle_kingside = False
                self.black_can_castle_queenside = False
                self.black_king_pos = (to_row, to_col)
                
        # If rook moves or is captured, update castling rights
        if piece.upper() == 'R':
            if self.current_player == ChessPlayer.WHITE.value:
                if from_row == 7 and from_col == 0:
                    self.white_can_castle_queenside = False
                elif from_row == 7 and from_col == 7:
                    self.white_can_castle_kingside = False
            else:
                if from_row == 0 and from_col == 0:
                    self.black_can_castle_queenside = False
                elif from_row == 0 and from_col == 7:
                    self.black_can_castle_kingside = False
                    
        if dest_piece.upper() == 'R':
            if to_row == 0 and to_col == 0:
                self.black_can_castle_queenside = False
            elif to_row == 0 and to_col == 7:
                self.black_can_castle_kingside = False
            elif to_row == 7 and to_col == 0:
                self.white_can_castle_queenside = False
            elif to_row == 7 and to_col == 7:
                self.white_can_castle_kingside = False
                
        # Perform the basic move
        super().perform_move(move)
        
        # Handle pawn promotion
        if piece.upper() == 'P' and (to_row == 0 or to_row == 7):
            promotion_piece = input("Promote to (Q/R/B/N): ").upper()
            if promotion_piece not in ['Q', 'R', 'B', 'N']:
                promotion_piece = 'Q'  # Default to queen
                
            if self.current_player == ChessPlayer.BLACK.value:
                promotion_piece = promotion_piece.lower()
                
            self.board.layout[to_row][to_col] = promotion_piece

    def game_finished(self):
        # Check for checkmate or stalemate
        for row in range(8):
            for col in range(8):
                piece = self.board.layout[row][col]
                if piece != '_' and self.get_piece_color(piece) == self.current_player:
                    # Check if this piece has any legal moves
                    for to_row in range(8):
                        for to_col in range(8):
                            move = f"{row},{col} {to_row},{to_col}"
                            if self.validate_move(move):
                                return False  # Found a legal move, game not finished
        
        # No legal moves - either checkmate or stalemate
        king_pos = self.white_king_pos if self.current_player == ChessPlayer.WHITE.value else self.black_king_pos
        
        # Check for 50-move rule
        if self.halfmove_clock >= 50:
            return True
            
        # Check for insufficient material
        if self.has_insufficient_material():
            return True
            
        return True  # No legal moves

    def has_insufficient_material(self):
        # Count pieces
        pieces = {'K': 0, 'k': 0, 'Q': 0, 'q': 0, 'R': 0, 'r': 0, 
                'B': 0, 'b': 0, 'N': 0, 'n': 0, 'P': 0, 'p': 0}
                
        for row in range(8):
            for col in range(8):
                piece = self.board.layout[row][col]
                if piece in pieces:
                    pieces[piece] += 1
                    
        # King vs King
        if (pieces['K'] == 1 and pieces['k'] == 1 and 
            sum(pieces.values()) == 2):
            return True
            
        # King and bishop vs King
        if ((pieces['K'] == 1 and pieces['B'] == 1 and pieces['k'] == 1) or
            (pieces['K'] == 1 and pieces['k'] == 1 and pieces['b'] == 1)) and \
            sum(pieces.values()) == 3:
            return True
            
        # King and knight vs King
        if ((pieces['K'] == 1 and pieces['N'] == 1 and pieces['k'] == 1) or
            (pieces['K'] == 1 and pieces['k'] == 1 and pieces['n'] == 1)) and \
            sum(pieces.values()) == 3:
            return True
            
        # King and bishop vs King and bishop (same color bishops)
        if pieces['K'] == 1 and pieces['B'] == 1 and pieces['k'] == 1 and pieces['b'] == 1 and \
           sum(pieces.values()) == 4:
            # Need to check if bishops are on the same color
            white_bishop_pos = None
            black_bishop_pos = None
            
            for row in range(8):
                for col in range(8):
                    if self.board.layout[row][col] == 'B':
                        white_bishop_pos = (row, col)
                    elif self.board.layout[row][col] == 'b':
                        black_bishop_pos = (row, col)
                        
            if white_bishop_pos and black_bishop_pos:
                white_square_color = (white_bishop_pos[0] + white_bishop_pos[1]) % 2
                black_square_color = (black_bishop_pos[0] + black_bishop_pos[1]) % 2
                
                if white_square_color == black_square_color:
                    return True
                    
        return False

    def get_winner(self):
        king_pos = self.white_king_pos if self.current_player == ChessPlayer.WHITE.value else self.black_king_pos
        
        # If current player's king is in check and there are no legal moves, it's checkmate
        if self.is_square_attacked(king_pos[0], king_pos[1], self.current_player):
            return ChessPlayer.BLACK.value if self.current_player == ChessPlayer.WHITE.value else ChessPlayer.WHITE.value
            
        # No legal moves but king is not in check, or insufficient material - it's a draw
        return None

    def finish_message(self, winner):
        if winner is None:
            print("The game is a draw!")
        else:
            winner_name = "White" if winner == ChessPlayer.WHITE.value else "Black"
            print(f"{winner_name} wins!")

if __name__ == '__main__':
    # Initialize the board with the modified layout (knights in center)
    # Modified layout with knights in the center instead of their usual positions
    layout = ("rnb_kbnr\n"  # Black back row (no knights)
              "pppppppp\n"  # Black pawns
              "________\n"  # Empty row
              "___nn___\n"  # Knights in center (black on c3, white on d3)
              "___NN___\n"  # Knights in center (black on c4, white on d4)
              "________\n"  # Empty row
              "PPPPPPPP\n"  # White pawns
              "RNB_KBNR")   # White back row (no knights)

    board = Board((8, 8), layout)
    chess_game = Chess(board)
    chess_game.game_loop()
