from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from enum import Enum

class Player(Enum):
    BLACK = 0
    WHITE = 1

class ReversiGame(Game):
    def __init__(self, board):
        super().__init__(board)
        self.black_king_used = False
        self.white_king_used = False
        self.current_player = self.initial_player()
        
    def initial_player(self):
        return Player.BLACK.value
        
    def prompt_current_player(self):
        player_name = "Black" if self.current_player == Player.BLACK.value else "White"
        king_status = ""
        if not (self.current_player == Player.BLACK.value and self.black_king_used) and \
           not (self.current_player == Player.WHITE.value and self.white_king_used):
            king_status = " (You can use 'K' for king)"
        return input(f"Player {player_name}'s move{king_status}: ")
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        try:
            if is_placement(move):
                piece, (row, col) = get_move_elements(move)
                
                # Validate king placement
                if piece.upper() == 'K':
                    if (self.current_player == Player.BLACK.value and self.black_king_used) or \
                       (self.current_player == Player.WHITE.value and self.white_king_used):
                        return False
                    piece = 'B' if self.current_player == Player.BLACK.value else 'W'
                
                # Validate regular piece placement
                elif piece not in ['B', 'W']:
                    return False
                    
                # Check if position is valid and empty
                if not (0 <= row < self.board.height and 0 <= col < self.board.width):
                    return False
                if self.board.layout[row, col] != '_':
                    return False
                    
                # Check if move flips at least one opponent piece
                return self.is_valid_placement(row, col, piece)
                
            elif is_movement(move):
                # Reversi doesn't use movement moves
                return False
                
        except (ValueError, IndexError):
            return False
            
        return False
        
    def is_valid_placement(self, row, col, piece):
        opponent = 'W' if piece == 'B' else 'B'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            
            while 0 <= r < self.board.height and 0 <= c < self.board.width:
                if self.board.layout[r, c] == opponent:
                    found_opponent = True
                    r += dr
                    c += dc
                elif self.board.layout[r, c] == piece and found_opponent:
                    return True
                else:
                    break
                    
        return False
        
    def perform_move(self, move):
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            
            # Handle king placement
            is_king = False
            if piece.upper() == 'K':
                is_king = True
                piece = 'B' if self.current_player == Player.BLACK.value else 'W'
                if self.current_player == Player.BLACK.value:
                    self.black_king_used = True
                else:
                    self.white_king_used = True
            
            # Place the piece
            self.board.place_piece(move)
            
            # Flip opponent's pieces
            self.flip_pieces(row, col, piece, is_king)
            
        super().perform_move(move)
        
    def flip_pieces(self, row, col, piece, is_king):
        opponent = 'W' if piece == 'B' else 'B'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            flip_candidates = []
            found_king = False
            
            while 0 <= r < self.board.height and 0 <= c < self.board.width:
                if self.board.layout[r, c] == opponent:
                    flip_candidates.append((r, c))
                    r += dr
                    c += dc
                elif self.board.layout[r, c] == piece:
                    # Check if king is in the line
                    for flip_r, flip_c in flip_candidates:
                        if self.board.layout[flip_r, flip_c] == 'K':
                            found_king = True
                            break
                    
                    # Flip pieces only if no king in the line
                    if not found_king:
                        for flip_r, flip_c in flip_candidates:
                            self.board.layout[flip_r, flip_c] = piece
                    break
                else:
                    break
                    
    def game_finished(self):
        # Check if board is full
        if '_' not in self.board.layout:
            return True
            
        # Check if both players have no valid moves
        black_moves = self.has_valid_moves('B')
        white_moves = self.has_valid_moves('W')
        
        return not black_moves and not white_moves
        
    def has_valid_moves(self, piece):
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == '_' and self.is_valid_placement(row, col, piece):
                    return True
        return False
        
    def get_winner(self):
        black_count = np.count_nonzero(self.board.layout == 'B')
        white_count = np.count_nonzero(self.board.layout == 'W')
        
        if black_count > white_count:
            return Player.BLACK.value
        elif white_count > black_count:
            return Player.WHITE.value
        else:
            return None
            
    def next_player(self):
        next_p = Player.WHITE.value if self.current_player == Player.BLACK.value else Player.BLACK.value
        
        # Check if next player has valid moves
        piece = 'B' if next_p == Player.BLACK.value else 'W'
        if self.has_valid_moves(piece):
            return next_p
        else:
            # Next player has no moves, return to current player
            return self.current_player
            
    def get_state(self):
        state = super().get_state()
        additional_params = [self.black_king_used, self.white_king_used]
        return (state[0], state[1], additional_params)

if __name__ == '__main__':
    # Create initial board with starting positions
    initial_layout = """________
________
________
___BW___
___WB___
________
________
________"""
    
    board = Board((8, 8), initial_layout)
    game = ReversiGame(board)
    game.game_loop()