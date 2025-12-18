from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class Saffron(Game):
    PLAYER_1 = 0
    PLAYER_2 = 1
    
    def __init__(self, board):
        super().__init__(board)
        # Initialize pieces in the center diagonally
        self.board.place_piece("A 3,3")
        self.board.place_piece("B 4,4")
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if not is_movement(move):
            return False
            
        (from_pos, to_pos) = get_move_elements(move)
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Check if moving own piece
        current_piece = self.board.layout[from_row, from_col]
        if (self.current_player == self.PLAYER_1 and current_piece != 'A') or \
           (self.current_player == self.PLAYER_2 and current_piece != 'B'):
            return False
            
        # Check if moving to opponent's piece
        target_piece = self.board.layout[to_row, to_col]
        if (self.current_player == self.PLAYER_1 and target_piece == 'B') or \
           (self.current_player == self.PLAYER_2 and target_piece == 'A'):
            return False
            
        # Check if moving to a marker (a or b)
        if target_piece in ['a', 'b']:
            return False
            
        # Check if orthogonal move (up, down, left, right)
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        if not ((row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)):
            return False
            
        return True
    
    def perform_move(self, move):
        (from_pos, to_pos) = get_move_elements(move)
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Place marker where piece was
        marker = 'a' if self.current_player == self.PLAYER_1 else 'b'
        self.board.place_piece(f"{marker} {from_row},{from_col}")
        
        # Move the piece
        self.board.move_piece(move)
    
    def game_finished(self):
        # The game ends immediately when a player moves onto a marker,
        # which is checked in validate_move, so we don't need to check here
        return False
    
    def get_winner(self):
        # The winner is determined when a player makes an invalid move (onto a marker)
        # This is handled in the game_loop by checking validate_move first
        return None
    
    def next_player(self):
        return self.PLAYER_2 if self.current_player == self.PLAYER_1 else self.PLAYER_1
    
    def prompt_current_player(self):
        player_name = "Player 1 (A)" if self.current_player == self.PLAYER_1 else "Player 2 (B)"
        return input(f"{player_name}'s move (format 'row,col row,col'): ")
    
    def finish_message(self, winner):
        if winner == self.PLAYER_1:
            print("Player 1 wins! Player 2 moved onto a marker.")
        else:
            print("Player 2 wins! Player 1 moved onto a marker.")

if __name__ == '__main__':
    board = Board((8, 8))
    game = Saffron(board)
    game.game_loop()