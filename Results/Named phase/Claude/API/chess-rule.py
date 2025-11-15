
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    WHITE = 0
    BLACK = 1

class Chess(Game):
    def __init__(self, board):
        super().__init__(board)
        self.castle_rights = {
            Player.WHITE: {'kingside': True, 'queenside': True},
            Player.BLACK: {'kingside': True, 'queenside': True}
        }
        self.en_passant_target = None
        self.last_pawn_double_move = None
        self.halfmove_clock = 0  # For 50-move rule
        self.fullmove_number = 1

    def initial_player(self):
        return Player.WHITE.value

    def next_player(self):
        return Player.BLACK.value if self.current_player == Player.WHITE.value else Player.WHITE.value
    
    def get_state(self):
        board_layout = deepcopy(self.board.layout)
        additional_params = [
            self.castle_rights,
            self.en_passant_target,
            self.halfmove_clock,
            self.fullmove_number
        ]
        return (board_layout, self.current_player, additional_params)
    
    def prompt_current_player(self):
        player_name = "White" if self.current_player == Player.WHITE.value else "Black"
        return input(f"{player_name}'s move: ")
    
    def get_piece_color(self, piece):
        if piece in 'PRNBQK':
            return Player.WHITE.value
        elif piece in 'prnbqk':
            return Player.BLACK.value
        return None
    
    def is_bishop_convert_pawn(self, move):
        """Check if the move is a bishop converting an adjacent pawn"""
        if not move.startswith("BC") and not move.startswith("bc"):
            return False
        
        # Format: BC x,y (bishop at x,y converts adjacent pawn)
        try:
            parts = move.split()
            bishop_pos = tuple(map(int, parts[1].split(',')))
            target_pos = tuple(map(int, parts[2].split(',')))
            
            # Check if bishop exists at the given position
            bishop = self.board.layout[bishop_pos[0]][bishop_pos[1]]
            if (self.current_player == Player.WHITE.value and bishop != 'B') or \
               (self.current_player == Player.BLACK.value and bishop != 'b'):
                return False
            
            # Check if target is horizontally adjacent
            if bishop_pos[0] != target_pos[0] or abs(bishop_pos[1] - target_pos[1]) != 1:
                return False
            
            # Check if target is opponent's pawn
            target = self.board.layout[target_pos[0]][target_pos[1]]
            return (self.current_player == Player.WHITE.value and target == 'p') or \
                   (self.current_player == Player.BLACK.value and target == 'P')
                   
        except (IndexError, ValueError):
            return False
    
    def is_queen_rook_swap(self, move):
        """Check if the move is a queen-rook swap"""
        if not move.startswith("QS") and not move.startswith("qs"):
            return False
        
        # Format: QS x1,y1 x2,y2 (queen at x1,y1 swaps with rook at x2,y2)
        try:
            parts = move.split()
            queen_pos = tuple(map(int, parts[1].split(',')))
            rook_pos = tuple(map(int, parts[2].split(',')))
            
            # Check if queen exists at the given position
            queen = self.board.layout[queen_pos[0]][queen_pos[1]]
            if (self.current_player == Player.WHITE.value and queen != 'Q') or \
               (self.current_player == Player.BLACK.value and queen != 'q'):
                return False
            
            # Check if rook exists at the given position and is same color
            rook = self.board.layout[rook_pos[0]][rook_pos[1]]
            if (self.current_player == Player.WHITE.value and rook != 'R') or \
               (self.current_player == Player.BLACK.value and rook != 'r'):
                return False
            
            # Check if both pieces are on the same color square
            # In chess, a square is black if the sum of its coordinates is odd
            queen_square_color = (queen_pos[0] + queen_pos[1]) % 2
            rook_square_color = (rook_pos[0] + rook_pos[1]) % 2
            
            return queen_square_color == rook_square_color
            
        except (IndexError, ValueError):
            return False
    
    def perform_bishop_convert(self, move):
        """Perform bishop conversion of opponent's pawn"""
        parts = move.split()
        bishop_pos = tuple(map(int, parts[1].split(',')))
        pawn_pos = tuple(map(int, parts[2].split(',')))
        
        # Convert the pawn to the bishop's color
        if self.current_player == Player.WHITE.value:
            self.board.layout[pawn_pos[0]][pawn_pos[1]] = 'P'
        else:
            self.board.layout[pawn_pos[0]][pawn_pos[1]] = 'p'
    
    def perform_queen_rook_swap(self, move):
        """Perform queen-rook swap"""
        parts = move.split()
        queen_pos = tuple(map(int, parts[1].split(',')))
        rook_pos = tuple(map(int, parts[2].split(',')))
        
        # Swap the pieces
        queen = self.board.layout[queen_pos[0]][queen_pos[1]]
        rook = self.board.layout[rook_pos[0]][rook_pos[1]]
        
        self.board.layout[queen_pos[0]][queen_pos[1]] = rook
        self.board.layout[rook_pos[0]][rook_pos[1]] = queen
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        # Check for custom moves first
        if self.is_bishop_convert_pawn(move) or self.is_queen_rook_swap(move):
            return True
            
        # Regular chess move validation
        if is_placement(move):
            return False  # In chess, pieces are not placed directly
            
        if is_movement(move):
            origin, dest = get_move_elements(move)
            
            # Check if origin is out of bounds
            if origin[0] < 0 or origin[0] >= self.board.height or origin[1] < 0 or origin[1] >= self.board.width:
                return False
                
            # Check if destination is out of bounds
            if dest[0] < 0 or dest[0] >= self.board.height or dest[1] < 0 or dest[1] >= self.board.width:
                return False
                
            # Check if there's a piece at the origin
            piece = self.board.layout[origin[0]][origin[1]]
            if piece == '_' or piece == ' ':
                return False
                
            # Check if the piece belongs to the current player
            if self.get_piece_color(piece) != self.current_player:
                return False
                
            # Check if destination has a piece of the same color
            dest_piece = self.board.layout[dest[0]][dest[1]]
            if dest_piece != '_' and self.get_piece_color(dest_piece) == self.current_player:
                return False
                
            # Validate specific piece movements
            piece_type = piece.upper()
            
            # Pawn movement
            if piece_type == 'P':
                return self.validate_pawn_move(origin, dest, piece)
                
            # Rook movement
            elif piece_type == 'R':
                return self.validate_rook_move(origin, dest)
                
            # Knight movement
            elif piece_type == 'N':
                return self.validate_knight_move(origin, dest)
                
            # Bishop movement
            elif piece_type == 'B':
                return self.validate_bishop_move(origin, dest)
                
            # Queen movement
            elif piece_type == 'Q':
                return self.validate_queen_move(origin, dest)
                
            # King movement (including castling)
            elif piece_type == 'K':
                return self.validate_king_move(origin, dest)
                
        return False
    
    def validate_pawn_move(self, origin, dest, piece):
        # Direction of movement depends on color
        direction = -1 if piece.isupper() else 1
        
        # Simple move forward
        if origin[1] == dest[1] and origin[0] + direction == dest[0] and self.board.layout[dest[0]][dest[1]] == '_':
            return True
            
        # Double move from starting position
        if origin[1] == dest[1] and ((piece.isupper() and origin[0] == 6 and dest[0] == 4) or 
                                     (piece.islower() and origin[0] == 1 and dest[0] == 3)):
            if self.board.layout[origin[0] + direction][origin[1]] == '_' and self.board.layout[dest[0]][dest[1]] == '_':
                return True
                
        # Capture
        if abs(origin[1] - dest[1]) == 1 and origin[0] + direction == dest[0]:
            # Regular capture
            if self.board.layout[dest[0]][dest[1]] != '_' and self.get_piece_color(self.board.layout[dest[0]][dest[1]]) != self.current_player:
                return True
                
            # En passant
            if self.en_passant_target and dest == self.en_passant_target:
                return True
                
        return False
    
    def validate_rook_move(self, origin, dest):
        # Rook moves horizontally or vertically
        if origin[0] != dest[0] and origin[1] != dest[1]:
            return False
            
        # Check if path is clear
        return self.is_path_clear(origin, dest)
    
    def validate_knight_move(self, origin, dest):
        # Knight moves in L-shape: 2 squares in one direction and 1 square perpendicular
        dx = abs(dest[0] - origin[0])
        dy = abs(dest[1] - origin[1])
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)
    
    def validate_bishop_move(self, origin, dest):
        # Bishop moves diagonally
        if abs(dest[0] - origin[0]) != abs(dest[1] - origin[1]):
            return False
            
        # Check if path is clear
        return self.is_path_clear(origin, dest)
    
    def validate_queen_move(self, origin, dest):
        # Queen moves like a rook or bishop
        if origin[0] == dest[0] or origin[1] == dest[1] or abs(dest[0] - origin[0]) == abs(dest[1] - origin[1]):
            return self.is_path_clear(origin, dest)
        return False
    
    def validate_king_move(self, origin, dest):
        # Regular king move (one square in any direction)
        dx = abs(dest[0] - origin[0])
        dy = abs(dest[1] - origin[1])
        
        if dx <= 1 and dy <= 1:
            return True
            
        # Castling
        if origin[0] == dest[0] and abs(dest[1] - origin[1]) == 2:
            player = Player.WHITE if self.current_player == Player.WHITE.value else Player.BLACK
            
            # Check if king is in starting position
            if (player == Player.WHITE and origin != (7, 4)) or (player == Player.BLACK and origin != (0, 4)):
                return False
                
            # Kingside castling
            if dest[1] > origin[1]:
                if not self.castle_rights[player]['kingside']:
                    return False
                rook_pos = (origin[0], 7)
                path_end = (origin[0], 6)
                
            # Queenside castling
            else:
                if not self.castle_rights[player]['queenside']:
                    return False
                rook_pos = (origin[0], 0)
                path_end = (origin[0], 2)
                
            # Check if path is clear
            if not self.is_path_clear(origin, rook_pos):
                return False
                
            # Check if king is in check or passes through check
            # (This would require a more complex check-detection function)
            
            return True
            
        return False
    
    def is_path_clear(self, origin, dest):
        # Determine direction of movement
        dx = 0 if dest[0] == origin[0] else (1 if dest[0] > origin[0] else -1)
        dy = 0 if dest[1] == origin[1] else (1 if dest[1] > origin[1] else -1)
        
        # Check each square in the path (excluding origin and including destination)
        x, y = origin[0] + dx, origin[1] + dy
        while (x, y) != dest:
            if self.board.layout[x][y] != '_':
                return False
            x += dx
            y += dy
            
        return True
    
    def perform_move(self, move):
        # Handle special moves
        if self.is_bishop_convert_pawn(move):
            self.perform_bishop_convert(move)
            self.halfmove_clock = 0  # Reset halfmove clock
            return
            
        if self.is_queen_rook_swap(move):
            self.perform_queen_rook_swap(move)
            return
            
        # Regular chess move
        if is_movement(move):
            origin, dest = get_move_elements(move)
            piece = self.board.layout[origin[0]][origin[1]]
            target = self.board.layout[dest[0]][dest[1]]
            
            # Reset en passant target
            prev_en_passant = self.en_passant_target
            self.en_passant_target = None
            
            # Handle castling
            if piece.upper() == 'K' and abs(dest[1] - origin[1]) == 2:
                # Kingside castling
                if dest[1] > origin[1]:
                    rook_origin = (origin[0], 7)
                    rook_dest = (origin[0], 5)
                # Queenside castling
                else:
                    rook_origin = (origin[0], 0)
                    rook_dest = (origin[0], 3)
                    
                # Move the rook
                rook = self.board.layout[rook_origin[0]][rook_origin[1]]
                self.board.layout[rook_dest[0]][rook_dest[1]] = rook
                self.board.layout[rook_origin[0]][rook_origin[1]] = '_'
                
            # Handle pawn moves
            if piece.upper() == 'P':
                # Double pawn move - set en passant target
                if abs(dest[0] - origin[0]) == 2:
                    self.en_passant_target = (origin[0] + (1 if piece.islower() else -1), origin[1])
                    
                # En passant capture
                elif dest == prev_en_passant:
                    # Remove the captured pawn
                    captured_pawn_pos = (origin[0], dest[1])
                    self.board.layout[captured_pawn_pos[0]][captured_pawn_pos[1]] = '_'
                    
                # Pawn promotion (to queen by default)
                if (piece.isupper() and dest[0] == 0) or (piece.islower() and dest[0] == 7):
                    piece = 'Q' if piece.isupper() else 'q'
                    
                self.halfmove_clock = 0  # Reset halfmove clock for pawn moves
                
            else:
                # Update halfmove clock - increment for non-pawn moves without capture
                if target == '_':
                    self.halfmove_clock += 1
                else:
                    self.halfmove_clock = 0  # Reset for captures
                    
            # Update castling rights if king or rook moves
            if piece.upper() == 'K':
                player = Player.WHITE if piece.isupper() else Player.BLACK
                self.castle_rights[player]['kingside'] = False
                self.castle_rights[player]['queenside'] = False
                
            elif piece.upper() == 'R':
                player = Player.WHITE if piece.isupper() else Player.BLACK
                # Kingside rook
                if origin == (7, 7) and player == Player.WHITE:
                    self.castle_rights[player]['kingside'] = False
                elif origin == (0, 7) and player == Player.BLACK:
                    self.castle_rights[player]['kingside'] = False
                # Queenside rook
                elif origin == (7, 0) and player == Player.WHITE:
                    self.castle_rights[player]['queenside'] = False
                elif origin == (0, 0) and player == Player.BLACK:
                    self.castle_rights[player]['queenside'] = False
                    
            # Execute the move
            self.board.move_piece(move)
            
            # Update the piece if it was a promotion
            if piece.upper() == 'P' and ((piece.isupper() and dest[0] == 0) or (piece.islower() and dest[0] == 7)):
                self.board.layout[dest[0]][dest[1]] = 'Q' if piece.isupper() else 'q'
                
            # Update fullmove counter (increments after Black's move)
            if self.current_player == Player.BLACK.value:
                self.fullmove_number += 1
    
    def game_finished(self):
        # Check for checkmate or stalemate - simplified version
        # In a full implementation, would need to check for:
        # 1. If the current player is in check
        # 2. If the current player has any legal moves
        # 3. Threefold repetition
        # 4. Fifty-move rule
        
        # Simplified check for kings
        white_king_exists = False
        black_king_exists = False
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row][col]
                if piece == 'K':
                    white_king_exists = True
                elif piece == 'k':
                    black_king_exists = True
                    
        # Game ends if either king is captured
        if not white_king_exists or not black_king_exists:
            return True
            
        # Check for 50-move rule
        if self.halfmove_clock >= 100:  # 50 moves = 100 half-moves
            return True
            
        # A more complete implementation would check for checkmate and stalemate
        
        return False
    
    def get_winner(self):
        # Check if kings exist
        white_king_exists = False
        black_king_exists = False
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row][col]
                if piece == 'K':
                    white_king_exists = True
                elif piece == 'k':
                    black_king_exists = True
        
        # If a king is missing, the other player wins
        if not white_king_exists:
            return Player.BLACK.value
        if not black_king_exists:
            return Player.WHITE.value
            
        # If 50-move rule is reached, it's a draw
        if self.halfmove_clock >= 100:
            return None
            
        # A more complete implementation would determine checkmate
        
        return None
    
    def finish_message(self, winner):
        if winner is None:
            print("Game ended in a draw!")
        else:
            winner_name = "White" if winner == Player.WHITE.value else "Black"
            print(f"{winner_name} wins the game!")

if __name__ == '__main__':
    # Initialize the chess board with standard setup
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
