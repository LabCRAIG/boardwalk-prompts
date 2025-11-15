from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np
from enum import Enum

class Player(Enum):
    NONE = 0
    PLAYER = 1

class PegSolitaire(Game):
    def __init__(self, board):
        super().__init__(board)
        self.pegs_remaining = np.count_nonzero(self.board.layout == 'O')
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if is_movement(move):
            origin, destination = get_move_elements(move)
            origin_row, origin_col = origin
            dest_row, dest_col = destination
            
            # Check if origin has a peg and destination is blank
            if (self.board.layout[origin_row, origin_col] != 'O' or 
                self.board.layout[dest_row, dest_col] != '_'):
                return False
                
            # Check if move is exactly two spaces in one direction
            row_diff = dest_row - origin_row
            col_diff = dest_col - origin_col
            
            # Must move exactly 2 spaces in one direction and 0 in the other
            if not ((abs(row_diff) == 2 and col_diff == 0) or 
                   (abs(col_diff) == 2 and row_diff == 0)):
                return False
                
            # Check if there's a peg to jump over
            jump_row = origin_row + row_diff // 2
            jump_col = origin_col + col_diff // 2
            
            if self.board.layout[jump_row, jump_col] != 'O':
                return False
                
            return True
            
        return False
        
    def perform_move(self, move):
        if is_movement(move):
            origin, destination = get_move_elements(move)
            origin_row, origin_col = origin
            dest_row, dest_col = destination
            
            # Move the peg
            self.board.move_piece(move)
            
            # Remove the jumped peg
            jump_row = origin_row + (dest_row - origin_row) // 2
            jump_col = origin_col + (dest_col - origin_col) // 2
            self.board.layout[jump_row, jump_col] = '_'
            
            self.pegs_remaining -= 1
            
    def game_finished(self):
        # Check if no more moves are possible
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == 'O':
                    # Check all possible jump directions
                    for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                        jump_row = row + dr // 2
                        jump_col = col + dc // 2
                        dest_row = row + dr
                        dest_col = col + dc
                        
                        if (0 <= dest_row < self.board.height and 
                            0 <= dest_col < self.board.width and
                            self.board.layout[dest_row, dest_col] == '_' and
                            self.board.layout[jump_row, jump_col] == 'O'):
                            return False
        return True
        
    def get_winner(self):
        if self.pegs_remaining == 1:
            return Player.PLAYER.value
        return Player.NONE.value
        
    def next_player(self):
        return Player.PLAYER.value
        
    def initial_player(self):
        return Player.PLAYER.value
        
    def prompt_current_player(self):
        return input(f"Pegs remaining: {self.pegs_remaining}. Your move (format: 'row,col row,col'): ")
        
    def finish_message(self, winner):
        if winner == Player.PLAYER.value:
            print("Congratulations! You won Peg Solitaire!")
        else:
            print(f"Game over! {self.pegs_remaining} pegs remaining.")

if __name__ == '__main__':
    # Create diamond-shaped board layout
    diamond_layout = (
        "  _  \n"
        " _O_ \n"
        "_O_O_\n"
        " _O_ \n"
        "  _  "
    )
    
    board = Board((5, 5), diamond_layout)
    mygame = PegSolitaire(board)
    mygame.game_loop()