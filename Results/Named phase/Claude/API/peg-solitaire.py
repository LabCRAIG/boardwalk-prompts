from game import Game, Board, is_movement, is_placement, get_move_elements
from enum import Enum
from copy import deepcopy

class PegSolitaire(Game):
    class Player(Enum):
        PLAYER = 0

    def __init__(self, board):
        super().__init__(board)
        self.pegs_remaining = sum(1 for row in self.board.layout for cell in row if cell == 'O')
        
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        # Only movements are allowed in Peg Solitaire
        if not is_movement(move):
            return False
            
        origin, destination = get_move_elements(move)
        origin_row, origin_col = origin
        dest_row, dest_col = destination
        
        # Check if origin has a peg and destination is empty
        if self.board.layout[origin_row][origin_col] != 'O' or self.board.layout[dest_row][dest_col] != '_':
            return False
            
        # Check if the move is exactly two spaces away (horizontally or vertically)
        row_diff = abs(dest_row - origin_row)
        col_diff = abs(dest_col - origin_col)
        
        # Must move exactly two spaces in one direction only
        if not ((row_diff == 2 and col_diff == 0) or (row_diff == 0 and col_diff == 2)):
            return False
            
        # Check if there's a peg in between (to jump over)
        middle_row = (origin_row + dest_row) // 2
        middle_col = (origin_col + dest_col) // 2
        
        if self.board.layout[middle_row][middle_col] != 'O':
            return False
            
        return True
        
    def perform_move(self, move):
        # Move the peg
        super().perform_move(move)
        
        # Remove the jumped peg
        origin, destination = get_move_elements(move)
        middle_row = (origin[0] + destination[0]) // 2
        middle_col = (origin[1] + destination[1]) // 2
        
        # Place a blank at the middle position (the jumped peg)
        self.board.place_piece(f"_ {middle_row},{middle_col}")
        
        # Update the count of remaining pegs
        self.pegs_remaining -= 1
        
    def game_finished(self):
        # Game is finished when no more valid moves are possible
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row][col] == 'O':
                    # Check all four possible jump directions
                    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
                    
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < self.board.height and 0 <= new_col < self.board.width:
                            move = f"{row},{col} {new_row},{new_col}"
                            if self.validate_move(move):
                                return False
        
        return True
        
    def get_winner(self):
        # In solitaire, you win if only one peg remains
        if self.pegs_remaining == 1:
            return self.Player.PLAYER.value
        else:
            return None
            
    def next_player(self):
        # Only one player in solitaire
        return self.Player.PLAYER.value
        
    def finish_message(self, winner):
        if winner is not None:
            print(f"Congratulations! You won with {self.pegs_remaining} peg remaining!")
        else:
            print(f"Game over. You ended with {self.pegs_remaining} pegs remaining.")
        
    def prompt_current_player(self):
        return input("Enter move (origin to destination, e.g. '3,3 3,5'): ")

if __name__ == '__main__':
    # English-style board layout with a hole in the center
    layout = """    OOO    
    OOO    
OOOOOOOOOOO
OOO_OOOOOOO
OOOOOOOOOOO
    OOO    
    OOO    """

    board = Board((7, 11), layout)
    game = PegSolitaire(board)
    game.game_loop()