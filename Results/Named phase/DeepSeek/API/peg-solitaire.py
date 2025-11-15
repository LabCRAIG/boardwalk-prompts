from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class PegSolitaire(Game):
    def __init__(self, board):
        super().__init__(board)
        self.pegs_remaining = 32  # Initial number of pegs in standard English board

    def prompt_current_player(self):
        print(f"Pegs remaining: {self.pegs_remaining}")
        return input("Your move (format 'from_row,from_col to_row,to_col'): ")

    def validate_move(self, move):
        if not is_movement(move):
            return False
        
        (from_pos, to_pos) = get_move_elements(move)
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Check bounds
        if not (0 <= from_row < self.board.height and 0 <= from_col < self.board.width and
                0 <= to_row < self.board.height and 0 <= to_col < self.board.width):
            return False
        
        # Check positions are valid (not null spaces)
        if (self.board.layout[from_row, from_col] == ' ' or 
            self.board.layout[to_row, to_col] == ' '):
            return False
        
        # Check from position has peg and to position is empty
        if (self.board.layout[from_row, from_col] != 'o' or 
            self.board.layout[to_row, to_col] != '_'):
            return False
        
        # Check it's a valid jump (2 spaces in straight line)
        row_diff = to_row - from_row
        col_diff = to_col - from_col
        
        if abs(row_diff) == 2 and col_diff == 0:  # Vertical jump
            mid_row = from_row + row_diff // 2
            if self.board.layout[mid_row, from_col] != 'o':
                return False
        elif abs(col_diff) == 2 and row_diff == 0:  # Horizontal jump
            mid_col = from_col + col_diff // 2
            if self.board.layout[from_row, mid_col] != 'o':
                return False
        else:
            return False
            
        return True

    def perform_move(self, move):
        (from_pos, to_pos) = get_move_elements(move)
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Move the peg
        self.board.move_piece(move)
        
        # Remove the jumped peg
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        self.board.place_piece(f'_ {mid_row},{mid_col}')
        
        self.pegs_remaining -= 1

    def game_finished(self):
        # Check if no more moves are possible
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == 'o':
                    # Check all possible jumps
                    for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        new_row, new_col = row + dr, col + dc
                        mid_row, mid_col = row + dr//2, col + dc//2
                        
                        if (0 <= new_row < self.board.height and 
                            0 <= new_col < self.board.width and
                            self.board.layout[new_row, new_col] == '_' and
                            self.board.layout[mid_row, mid_col] == 'o'):
                            return False
        return True

    def get_winner(self):
        # In Peg Solitaire, the goal is to have as few pegs as possible
        # We'll consider 1 peg remaining as a win
        if self.pegs_remaining == 1:
            return 1  # Player wins
        return None  # Game lost or still in progress

    def finish_message(self, winner):
        if winner == 1:
            print("Congratulations! You won with 1 peg remaining!")
        else:
            print(f"Game over! You finished with {self.pegs_remaining} pegs remaining.")

if __name__ == '__main__':
    # Standard English board layout
    layout = (
        "  ooo  \n"
        "  ooo  \n"
        "ooooooo\n"
        "ooo_ooo\n"
        "ooooooo\n"
        "  ooo  \n"
        "  ooo  "
    )
    board = Board((7, 7), layout)
    game = PegSolitaire(board)
    game.game_loop()