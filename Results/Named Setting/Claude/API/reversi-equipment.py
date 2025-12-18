
from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class Player(Enum):
    BLACK = 0
    WHITE = 1

class Reversi(Game):
    def __init__(self, board: Board):
        super().__init__(board)
        self.current_player = self.initial_player()
        self.place_initial_pieces()
        
    def initial_player(self):
        return Player.BLACK.value
    
    def place_initial_pieces(self):
        # Initial 4 pieces in the center
        center_x = self.board.width // 2
        center_y = self.board.height // 2
        
        self.board.place_piece(f"B {center_y-1},{center_x-1}")
        self.board.place_piece(f"W {center_y-1},{center_x}")
        self.board.place_piece(f"W {center_y},{center_x-1}")
        self.board.place_piece(f"B {center_y},{center_x}")
    
    def prompt_current_player(self):
        player_symbol = 'B' if self.current_player == Player.BLACK.value else 'W'
        return input(f"Player {player_symbol}'s move (row,col): ")
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if not is_placement(move):
            return False
            
        piece, pos = get_move_elements(move)
        row, col = pos
        
        # Check if position is in a corner 2x2 square
        if (row < 2 and col < 2) or \
           (row < 2 and col >= self.board.width - 2) or \
           (row >= self.board.height - 2 and col < 2) or \
           (row >= self.board.height - 2 and col >= self.board.width - 2):
            return False
        
        # Check if position is already occupied
        if self.board.layout[row][col] != '_':
            return False
        
        # Check if the move flips at least one opponent piece
        player_symbol = 'B' if self.current_player == Player.BLACK.value else 'W'
        opponent_symbol = 'W' if player_symbol == 'B' else 'B'
        
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        valid_move = False
        for dr, dc in directions:
            r, c = row + dr, col + dc
            # Check if the first adjacent piece is opponent's
            if (0 <= r < self.board.height and 
                0 <= c < self.board.width and 
                self.board.layout[r][c] == opponent_symbol):
                
                # Continue in this direction to find if there's a flanking piece
                r += dr
                c += dc
                while (0 <= r < self.board.height and 
                       0 <= c < self.board.width):
                    if self.board.layout[r][c] == '_':
                        break
                    if self.board.layout[r][c] == player_symbol:
                        valid_move = True
                        break
                    r += dr
                    c += dc
        
        return valid_move
    
    def perform_move(self, move):
        piece, pos = get_move_elements(move)
        row, col = pos
        
        # Place the player's piece
        player_symbol = 'B' if self.current_player == Player.BLACK.value else 'W'
        self.board.place_piece(f"{player_symbol} {row},{col}")
        
        # Flip opponent's pieces
        opponent_symbol = 'W' if player_symbol == 'B' else 'B'
        
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dr, dc in directions:
            pieces_to_flip = []
            r, c = row + dr, col + dc
            
            # Check if the first adjacent piece is opponent's
            if (0 <= r < self.board.height and 
                0 <= c < self.board.width and 
                self.board.layout[r][c] == opponent_symbol):
                
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
                
                # Continue in this direction to find if there's a flanking piece
                while (0 <= r < self.board.height and 
                       0 <= c < self.board.width):
                    if self.board.layout[r][c] == '_':
                        pieces_to_flip = []
                        break
                    if self.board.layout[r][c] == player_symbol:
                        break
                    pieces_to_flip.append((r, c))
                    r += dr
                    c += dc
                
                # If we found a flanking piece, flip all pieces in between
                if (0 <= r < self.board.height and 
                    0 <= c < self.board.width and 
                    self.board.layout[r][c] == player_symbol):
                    for flip_r, flip_c in pieces_to_flip:
                        self.board.place_piece(f"{player_symbol} {flip_r},{flip_c}")
    
    def game_finished(self):
        # Game is finished if neither player can make a valid move
        current_player_backup = self.current_player
        
        # Check if current player can make a move
        current_can_move = self.has_valid_moves()
        
        # Check if other player can make a move
        self.current_player = 1 - self.current_player
        other_can_move = self.has_valid_moves()
        
        # Restore current player
        self.current_player = current_player_backup
        
        return not (current_can_move or other_can_move)
    
    def has_valid_moves(self):
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row][col] == '_':
                    player_symbol = 'B' if self.current_player == Player.BLACK.value else 'W'
                    move = f"{player_symbol} {row},{col}"
                    if self.validate_move(move):
                        return True
        return False
    
    def get_winner(self):
        # Count pieces
        black_count = 0
        white_count = 0
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row][col] == 'B':
                    black_count += 1
                elif self.board.layout[row][col] == 'W':
                    white_count += 1
        
        if black_count > white_count:
            return Player.BLACK.value
        elif white_count > black_count:
            return Player.WHITE.value
        else:
            return None  # Draw
    
    def next_player(self):
        next_player = 1 - self.current_player
        
        # Check if next player has valid moves
        self.current_player = next_player
        if self.has_valid_moves():
            self.current_player = next_player
            return next_player
        
        # If next player can't move, keep current player
        self.current_player = 1 - next_player
        return 1 - next_player
    
    def finish_message(self, winner):
        black_count = 0
        white_count = 0
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row][col] == 'B':
                    black_count += 1
                elif self.board.layout[row][col] == 'W':
                    white_count += 1
                    
        if winner == Player.BLACK.value:
            print(f"Black wins with {black_count} pieces to {white_count}!")
        elif winner == Player.WHITE.value:
            print(f"White wins with {white_count} pieces to {black_count}!")
        else:
            print(f"It's a draw! Both players have {black_count} pieces.")

if __name__ == '__main__':
    board = Board((8, 8))
    game = Reversi(board)
    game.game_loop()
