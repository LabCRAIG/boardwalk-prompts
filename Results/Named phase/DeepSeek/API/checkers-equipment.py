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
        self.captured_pieces = {Player.RED: 0, Player.BLACK: 0}
        
    def initial_player(self):
        return Player.RED.value
        
    def prompt_current_player(self):
        player_name = "RED" if self.current_player == Player.RED.value else "BLACK"
        return input(f"Player {player_name}, enter your move: ")
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if is_movement(move):
            origin, destination = get_move_elements(move)
            origin_row, origin_col = origin
            dest_row, dest_col = destination
            
            # Check if origin has a piece that belongs to current player
            piece = self.board.layout[origin_row, origin_col]
            if self.current_player == Player.RED.value and piece not in ['r', 'R']:
                return False
            if self.current_player == Player.BLACK.value and piece not in ['b', 'B']:
                return False
                
            # Check if destination is blank
            if self.board.layout[dest_row, dest_col] != '_':
                return False
                
            # Check if move is diagonal
            row_diff = abs(dest_row - origin_row)
            col_diff = abs(dest_col - origin_col)
            
            if row_diff != col_diff:
                return False
                
            # Regular move (one space)
            if row_diff == 1:
                # Check direction for regular pieces
                if piece in ['r', 'b']:
                    if self.current_player == Player.RED.value and dest_row <= origin_row:
                        return False
                    if self.current_player == Player.BLACK.value and dest_row >= origin_row:
                        return False
                return True
                
            # Jump move (two spaces - capture)
            elif row_diff == 2:
                # Find the jumped piece
                jump_row = (origin_row + dest_row) // 2
                jump_col = (origin_col + dest_col) // 2
                jumped_piece = self.board.layout[jump_row, jump_col]
                
                # Check if jumped piece belongs to opponent
                if self.current_player == Player.RED.value and jumped_piece not in ['b', 'B']:
                    return False
                if self.current_player == Player.BLACK.value and jumped_piece not in ['r', 'R']:
                    return False
                    
                # Check direction for regular pieces
                if piece in ['r', 'b']:
                    if self.current_player == Player.RED.value and dest_row <= origin_row:
                        return False
                    if self.current_player == Player.BLACK.value and dest_row >= origin_row:
                        return False
                return True
                
        return False
        
    def perform_move(self, move):
        if is_movement(move):
            origin, destination = get_move_elements(move)
            origin_row, origin_col = origin
            dest_row, dest_col = destination
            
            piece = self.board.layout[origin_row, origin_col]
            
            # Check if this is a capture move
            row_diff = abs(dest_row - origin_row)
            if row_diff == 2:
                # Remove the captured piece
                jump_row = (origin_row + dest_row) // 2
                jump_col = (origin_col + dest_col) // 2
                captured_piece = self.board.layout[jump_row, jump_col]
                self.board.layout[jump_row, jump_col] = '_'
                
                # Update capture count
                if captured_piece in ['r', 'R']:
                    self.captured_pieces[Player.RED] += 1
                else:
                    self.captured_pieces[Player.BLACK] += 1
            
            # Move the piece
            self.board.move_piece(move)
            
            # Check for promotion to king
            if piece == 'r' and dest_row == self.board.height - 1:
                self.board.layout[dest_row, dest_col] = 'R'
            elif piece == 'b' and dest_row == 0:
                self.board.layout[dest_row, dest_col] = 'B'
                
    def game_finished(self):
        # Game ends if one player has no pieces or cannot move
        red_pieces = np.count_nonzero((self.board.layout == 'r') | (self.board.layout == 'R'))
        black_pieces = np.count_nonzero((self.board.layout == 'b') | (self.board.layout == 'B'))
        
        if red_pieces == 0 or black_pieces == 0:
            return True
            
        # Check if current player has any valid moves
        current_player_pieces = []
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.layout[row, col]
                if (self.current_player == Player.RED.value and piece in ['r', 'R']) or \
                   (self.current_player == Player.BLACK.value and piece in ['b', 'B']):
                    current_player_pieces.append((row, col))
        
        for row, col in current_player_pieces:
            # Check all possible diagonal moves
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.board.height and 0 <= new_col < self.board.width:
                    move_str = f"{row},{col} {new_row},{new_col}"
                    if self.validate_move(move_str):
                        return False
                        
            # Check all possible jump moves
            for dr, dc in [(2, 2), (2, -2), (-2, 2), (-2, -2)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.board.height and 0 <= new_col < self.board.width:
                    move_str = f"{row},{col} {new_row},{new_col}"
                    if self.validate_move(move_str):
                        return False
        
        return True
        
    def get_winner(self):
        red_pieces = np.count_nonzero((self.board.layout == 'r') | (self.board.layout == 'R'))
        black_pieces = np.count_nonzero((self.board.layout == 'b') | (self.board.layout == 'B'))
        
        if red_pieces == 0:
            return Player.BLACK.value
        elif black_pieces == 0:
            return Player.RED.value
            
        # If no moves available for current player, opponent wins
        return 1 - self.current_player
        
    def next_player(self):
        # In checkers, players alternate turns
        return 1 - self.current_player
        
    def finish_message(self, winner):
        if winner is None:
            print("The game ended in a draw!")
        else:
            winner_name = "RED" if winner == Player.RED.value else "BLACK"
            print(f"Player {winner_name} wins!")

if __name__ == '__main__':
    # Create initial board layout for checkers
    # 'r' = red piece, 'b' = black piece, '_' = empty space
    # Kings will be represented as 'R' and 'B'
    layout_str = ""
    for row in range(8):
        for col in range(8):
            if row < 2:
                layout_str += 'b'  # Black pieces at top
            elif row > 5:
                layout_str += 'r'  # Red pieces at bottom
            else:
                layout_str += '_'  # Empty spaces in middle
        if row < 7:
            layout_str += '\n'
    
    board = Board((8, 8), layout_str)
    mygame = Checkers(board)
    mygame.game_loop()