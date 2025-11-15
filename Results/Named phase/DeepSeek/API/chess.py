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
        self.promotion_pieces = {'Q', 'R', 'B', 'N', 'q', 'r', 'b', 'n'}

    def initial_player(self):
        return Player.WHITE.value

    def prompt_current_player(self):
        player_name = "White" if self.current_player == Player.WHITE.value else "Black"
        return input(f"Player {player_name}, enter your move: ").strip()

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
        # Placement only used for pawn promotion
        if self.board.layout[from_row, from_col] not in {'P', 'p'}:
            return False
        if piece not in self.promotion_pieces:
            return False
        if (self.current_player == Player.WHITE.value and row != 0) or \
           (self.current_player == Player.BLACK.value and row != 7):
            return False
        return True

    def is_valid_movement(self, from_row, from_col, to_row, to_col):
        piece = self.board.layout[from_row, from_col]
        
        # Check if piece belongs to current player
        if self.current_player == Player.WHITE.value and not piece.isupper():
            return False
        if self.current_player == Player.BLACK.value and not piece.islower():
            return False
        if piece == '_' or piece == ' ':
            return False

        # Check destination piece
        target = self.board.layout[to_row, to_col]
        if target != '_' and target != ' ':
            if (self.current_player == Player.WHITE.value and target.isupper()) or \
               (self.current_player == Player.BLACK.value and target.islower()):
                return False

        # Piece-specific movement rules
        if piece.upper() == 'P':
            return self.is_valid_pawn_move(from_row, from_col, to_row, to_col)
        elif piece.upper() == 'R':
            return self.is_valid_rook_move(from_row, from_col, to_row, to_col)
        elif piece.upper() == 'N':
            return self.is_valid_knight_move(from_row, from_col, to_row, to_col)
        elif piece.upper() == 'B':
            return self.is_valid_bishop_move(from_row, from_col, to_row, to_col)
        elif piece.upper() == 'Q':
            return self.is_valid_queen_move(from_row, from_col, to_row, to_col)
        elif piece.upper() == 'K':
            return self.is_valid_king_move(from_row, from_col, to_row, to_col)
        return False

    def is_valid_pawn_move(self, from_row, from_col, to_row, to_col):
        direction = -1 if self.current_player == Player.WHITE.value else 1
        start_row = 6 if self.current_player == Player.WHITE.value else 1
        
        # Forward move
        if from_col == to_col:
            if to_row == from_row + direction and self.board.layout[to_row, to_col] == '_':
                return True
            if from_row == start_row and to_row == from_row + 2*direction and \
               self.board.layout[from_row + direction, from_col] == '_' and \
               self.board.layout[to_row, to_col] == '_':
                return True
        
        # Capture
        if abs(from_col - to_col) == 1 and to_row == from_row + direction:
            target = self.board.layout[to_row, to_col]
            if target != '_' and target != ' ':
                return True
            # En passant
            if self.en_passant_target == (to_row, to_col):
                return True
        
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
        return self.is_valid_rook_move(from_row, from_col, to_row, to_col) or \
               self.is_valid_bishop_move(from_row, from_col, to_row, to_col)

    def is_valid_king_move(self, from_row, from_col, to_row, to_col):
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        
        # Normal king move
        if row_diff <= 1 and col_diff <= 1:
            return True
        
        # Castling
        if from_row == to_row and abs(from_col - to_col) == 2:
            return self.is_valid_castling(from_row, from_col, to_col)
        
        return False

    def is_valid_castling(self, row, from_col, to_col):
        side = 'K' if to_col > from_col else 'Q'
        castle_key = side if self.current_player == Player.WHITE.value else side.lower()
        
        if not self.castling_rights[castle_key]:
            return False
        
        # Check if path is clear and not in check
        direction = 1 if side == 'K' else -1
        for col in range(from_col + direction, from_col + 3*direction, direction):
            if self.board.layout[row, col] != '_':
                return False
            # Simulate move to check for check
            if self.would_be_in_check(row, from_col, row, col):
                return False
        
        return True

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

    def would_be_in_check(self, from_row, from_col, to_row, to_col):
        # Simulate move and check if king would be in check
        temp_board = self.board.layout.copy()
        piece = temp_board[from_row, from_col]
        temp_board[to_row, to_col] = piece
        temp_board[from_row, from_col] = '_'
        
        # Find king position
        king_char = 'K' if self.current_player == Player.WHITE.value else 'k'
        king_pos = None
        for i in range(8):
            for j in range(8):
                if temp_board[i, j] == king_char:
                    king_pos = (i, j)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        # Check if any opponent piece can capture the king
        opponent = Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value
        for i in range(8):
            for j in range(8):
                piece = temp_board[i, j]
                if piece != '_' and piece != ' ':
                    piece_player = Player.WHITE.value if piece.isupper() else Player.BLACK.value
                    if piece_player == opponent:
                        if self.can_capture(temp_board, i, j, king_pos[0], king_pos[1]):
                            return True
        return False

    def can_capture(self, board, from_row, from_col, to_row, to_col):
        piece = board[from_row, from_col].upper()
        if piece == 'P':
            direction = -1 if board[from_row, from_col].isupper() else 1
            return abs(from_col - to_col) == 1 and to_row == from_row + direction
        elif piece == 'R':
            return self.is_valid_rook_move(from_row, from_col, to_row, to_col) and \
                   self.is_path_clear(from_row, from_col, to_row, to_col)
        elif piece == 'N':
            return self.is_valid_knight_move(from_row, from_col, to_row, to_col)
        elif piece == 'B':
            return self.is_valid_bishop_move(from_row, from_col, to_row, to_col) and \
                   self.is_path_clear(from_row, from_col, to_row, to_col)
        elif piece == 'Q':
            return self.is_valid_queen_move(from_row, from_col, to_row, to_col) and \
                   self.is_path_clear(from_row, from_col, to_row, to_col)
        elif piece == 'K':
            return abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1
        return False

    def perform_move(self, move):
        if is_movement(move):
            (from_row, from_col), (to_row, to_col) = get_move_elements(move)
            piece = self.board.layout[from_row, from_col]
            
            # Handle castling
            if piece.upper() == 'K' and abs(from_col - to_col) == 2:
                self.handle_castling(from_row, from_col, to_col)
            else:
                self.board.move_piece(move)
                
                # Handle en passant capture
                if piece.upper() == 'P' and self.en_passant_target == (to_row, to_col) and from_col != to_col:
                    capture_row = from_row
                    self.board.layout[capture_row, to_col] = '_'
                
                # Handle pawn promotion
                if piece.upper() == 'P' and (to_row == 0 or to_row == 7):
                    promotion_piece = input("Promote to (Q/R/B/N): ").strip().upper()
                    if self.current_player == Player.BLACK.value:
                        promotion_piece = promotion_piece.lower()
                    self.board.place_piece(f"{promotion_piece} {to_row},{to_col}")
            
            # Update en passant target
            if piece.upper() == 'P' and abs(from_row - to_row) == 2:
                self.en_passant_target = ((from_row + to_row) // 2, from_col)
            else:
                self.en_passant_target = None
            
            # Update castling rights
            if piece.upper() == 'K':
                if self.current_player == Player.WHITE.value:
                    self.castling_rights['K'] = False
                    self.castling_rights['Q'] = False
                else:
                    self.castling_rights['k'] = False
                    self.castling_rights['q'] = False
            elif piece.upper() == 'R':
                if from_row == 7:
                    if from_col == 0:
                        self.castling_rights['Q'] = False
                    elif from_col == 7:
                        self.castling_rights['K'] = False
                elif from_row == 0:
                    if from_col == 0:
                        self.castling_rights['q'] = False
                    elif from_col == 7:
                        self.castling_rights['k'] = False

        # Update move counters
        if self.current_player == Player.BLACK.value:
            self.fullmove_number += 1
        self.halfmove_clock += 1

    def handle_castling(self, row, from_col, to_col):
        rook_from_col = 7 if to_col > from_col else 0
        rook_to_col = from_col + 1 if to_col > from_col else from_col - 1
        self.board.move_piece(f"{row},{from_col} {row},{to_col}")
        self.board.move_piece(f"{row},{rook_from_col} {row},{rook_to_col}")

    def game_finished(self):
        # Check for checkmate or stalemate
        if self.is_in_checkmate() or self.is_in_stalemate():
            return True
        
        # Check for insufficient material
        if self.is_insufficient_material():
            return True
        
        # Check for 50-move rule
        if self.halfmove_clock >= 100:
            return True
        
        return False

    def is_in_checkmate(self):
        if not self.is_king_in_check():
            return False
        
        # Check if any move can get out of check
        for from_row in range(8):
            for from_col in range(8):
                piece = self.board.layout[from_row, from_col]
                if piece != '_' and piece != ' ':
                    piece_player = Player.WHITE.value if piece.isupper() else Player.BLACK.value
                    if piece_player == self.current_player:
                        for to_row in range(8):
                            for to_col in range(8):
                                if self.is_valid_movement(from_row, from_col, to_row, to_col):
                                    if not self.would_be_in_check(from_row, from_col, to_row, to_col):
                                        return False
        return True

    def is_in_stalemate(self):
        if self.is_king_in_check():
            return False
        
        # Check if any legal move exists
        for from_row in range(8):
            for from_col in range(8):
                piece = self.board.layout[from_row, from_col]
                if piece != '_' and piece != ' ':
                    piece_player = Player.WHITE.value if piece.isupper() else Player.BLACK.value
                    if piece_player == self.current_player:
                        for to_row in range(8):
                            for to_col in range(8):
                                if self.is_valid_movement(from_row, from_col, to_row, to_col):
                                    if not self.would_be_in_check(from_row, from_col, to_row, to_col):
                                        return False
        return True

    def is_king_in_check(self):
        king_char = 'K' if self.current_player == Player.WHITE.value else 'k'
        king_pos = None
        for i in range(8):
            for j in range(8):
                if self.board.layout[i, j] == king_char:
                    king_pos = (i, j)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        opponent = Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value
        for i in range(8):
            for j in range(8):
                piece = self.board.layout[i, j]
                if piece != '_' and piece != ' ':
                    piece_player = Player.WHITE.value if piece.isupper() else Player.BLACK.value
                    if piece_player == opponent:
                        if self.can_capture(self.board.layout, i, j, king_pos[0], king_pos[1]):
                            return True
        return False

    def is_insufficient_material(self):
        # Count pieces
        pieces = {'K': 0, 'Q': 0, 'R': 0, 'B': 0, 'N': 0, 'P': 0,
                  'k': 0, 'q': 0, 'r': 0, 'b': 0, 'n': 0, 'p': 0}
        
        for i in range(8):
            for j in range(8):
                piece = self.board.layout[i, j]
                if piece != '_' and piece != ' ':
                    pieces[piece] += 1
        
        # King vs King
        if sum(pieces.values()) == 2:
            return True
        
        # King and bishop vs King
        # King and knight vs King
        if sum(pieces.values()) == 3:
            if (pieces['B'] == 1 and all(pieces[p] == 0 for p in ['Q', 'R', 'N', 'P'])) or \
               (pieces['b'] == 1 and all(pieces[p] == 0 for p in ['q', 'r', 'n', 'p'])) or \
               (pieces['N'] == 1 and all(pieces[p] == 0 for p in ['Q', 'R', 'B', 'P'])) or \
               (pieces['n'] == 1 and all(pieces[p] == 0 for p in ['q', 'r', 'b', 'p'])):
                return True
        
        return False

    def get_winner(self):
        if self.is_in_checkmate():
            return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value
        return None

    def next_player(self):
        return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value

    def round_counter(self):
        return self.round + 1

    def get_state(self):
        state = super().get_state()
        additional_params = [
            self.castling_rights.copy(),
            self.en_passant_target,
            self.halfmove_clock,
            self.fullmove_number
        ]
        return (state[0], state[1], additional_params)

    def finish_message(self, winner):
        if winner is None:
            print("The game ended in a draw!")
        else:
            winner_name = "White" if winner == Player.WHITE.value else "Black"
            print(f"Player {winner_name} wins!")

if __name__ == '__main__':
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