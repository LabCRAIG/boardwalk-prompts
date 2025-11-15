from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from copy import deepcopy

class Reversi(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Black starts
        self.round = 1
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if is_placement(move):
            piece, (row, col) = get_move_elements(move)
            
            # Check if position is in forbidden corner squares
            if self._is_forbidden_corner(row, col):
                return False
                
            # Check if position is empty
            if self.board.layout[row, col] != '_':
                return False
                
            # Check if move flips at least one opponent piece
            return self._has_valid_flips(row, col)
            
        return False
        
    def _is_forbidden_corner(self, row, col):
        height, width = self.board.height, self.board.width
        corners = [
            (0, 0), (0, 1), (1, 0), (1, 1),  # Top-left
            (0, width-2), (0, width-1), (1, width-2), (1, width-1),  # Top-right
            (height-2, 0), (height-1, 0), (height-2, 1), (height-1, 1),  # Bottom-left
            (height-2, width-2), (height-2, width-1), (height-1, width-2), (height-1, width-1)  # Bottom-right
        ]
        return (row, col) in corners
        
    def _has_valid_flips(self, row, col):
        opponent = 'W' if self.current_player == 1 else 'B'
        player_piece = 'B' if self.current_player == 1 else 'W'
        
        directions = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1),  (1, 0),  (1, 1)]
                     
        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            
            while (0 <= r < self.board.height and 0 <= c < self.board.width and 
                   self.board.layout[r, c] == opponent):
                r += dr
                c += dc
                found_opponent = True
                
            if (found_opponent and 0 <= r < self.board.height and 0 <= c < self.board.width and 
                self.board.layout[r, c] == player_piece):
                return True
                
        return False
        
    def perform_move(self, move):
        piece, (row, col) = get_move_elements(move)
        player_piece = 'B' if self.current_player == 1 else 'W'
        self.board.place_piece(f"{player_piece} {row},{col}")
        self._flip_pieces(row, col)
        
    def _flip_pieces(self, row, col):
        opponent = 'W' if self.current_player == 1 else 'B'
        player_piece = 'B' if self.current_player == 1 else 'W'
        
        directions = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1),  (1, 0),  (1, 1)]
                     
        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []
            
            while (0 <= r < self.board.height and 0 <= c < self.board.width and 
                   self.board.layout[r, c] == opponent):
                to_flip.append((r, c))
                r += dr
                c += dc
                
            if (0 <= r < self.board.height and 0 <= c < self.board.width and 
                self.board.layout[r, c] == player_piece):
                for flip_r, flip_c in to_flip:
                    self.board.place_piece(f"{player_piece} {flip_r},{flip_c}")
                    
    def game_finished(self):
        # Check if board is full or no valid moves for either player
        if np.count_nonzero(self.board.layout == '_') == 0:
            return True
            
        # Check if current player has no valid moves
        if not self._has_any_valid_moves():
            # Check if opponent also has no valid moves
            self.current_player = 3 - self.current_player  # Switch player
            opponent_has_moves = self._has_any_valid_moves()
            self.current_player = 3 - self.current_player  # Switch back
            return not opponent_has_moves
            
        return False
        
    def _has_any_valid_moves(self):
        empty_cells = np.where(self.board.layout == '_')
        for row, col in zip(empty_cells[0], empty_cells[1]):
            if not self._is_forbidden_corner(row, col) and self._has_valid_flips(row, col):
                return True
        return False
        
    def get_winner(self):
        black_count = np.count_nonzero(self.board.layout == 'B')
        white_count = np.count_nonzero(self.board.layout == 'W')
        
        if black_count > white_count:
            return 1
        elif white_count > black_count:
            return 2
        else:
            return None
            
    def next_player(self):
        return 3 - self.current_player  # Switch between 1 and 2
        
    def prompt_current_player(self):
        player_name = "Black" if self.current_player == 1 else "White"
        return input(f"Player {player_name}'s move (row,col): ")
        
    def get_state(self):
        state = super().get_state()
        return (deepcopy(self.board.layout), self.current_player, [])
        
    def finish_message(self, winner):
        if winner is None:
            print("The game is a draw!")
        else:
            winner_name = "Black" if winner == 1 else "White"
            print(f"Player {winner_name} wins!")

if __name__ == '__main__':
    # Create 8x8 board with initial Reversi setup
    initial_layout = """________
________
________
___BW___
___WB___
________
________
________"""
    
    board = Board((8, 8), initial_layout)
    mygame = Reversi(board)
    mygame.game_loop()