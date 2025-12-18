from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class PegSolitaire(Game):
    def __init__(self, board):
        super().__init__(board)
        self.moves_made = 0
        
    def prompt_current_player(self):
        return input("Enter your move (format 'from_row,from_col to_row,to_col'): ")
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if not is_movement(move):
            return False
            
        try:
            (from_pos, to_pos) = get_move_elements(move)
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            # Check if positions are within bounds
            if (from_row < 0 or from_row >= self.board.height or 
                from_col < 0 or from_col >= self.board.width or
                to_row < 0 or to_row >= self.board.height or
                to_col < 0 or to_col >= self.board.width):
                return False
                
            # Check if moving from a peg and to a blank space
            if (self.board.layout[from_row, from_col] != 'P' or 
                self.board.layout[to_row, to_col] != '_'):
                return False
                
            # Check if it's a valid jump (2 spaces in one direction)
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            
            if not ((row_diff == 2 and col_diff == 0) or (row_diff == 0 and col_diff == 2)):
                return False
                
            # Check if there's a peg to jump over
            jump_row = (from_row + to_row) // 2
            jump_col = (from_col + to_col) // 2
            
            if (jump_row < 0 or jump_row >= self.board.height or 
                jump_col < 0 or jump_col >= self.board.width):
                return False
                
            if self.board.layout[jump_row, jump_col] != 'P':
                return False
                
            return True
            
        except (ValueError, IndexError):
            return False
    
    def perform_move(self, move):
        (from_pos, to_pos) = get_move_elements(move)
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Move the peg
        self.board.move_piece(move)
        
        # Remove the jumped peg
        jump_row = (from_row + to_row) // 2
        jump_col = (from_col + to_col) // 2
        self.board.place_piece(f"_ {jump_row},{jump_col}")
        
        self.moves_made += 1
    
    def game_finished(self):
        # Count remaining pegs
        peg_count = np.count_nonzero(self.board.layout == 'P')
        
        # Game is won when only 2 pegs remain that cannot capture each other
        if peg_count == 2:
            # Find the two remaining pegs
            peg_positions = np.where(self.board.layout == 'P')
            pegs = list(zip(peg_positions[0], peg_positions[1]))
            
            # Check if they can capture each other
            peg1, peg2 = pegs
            row_diff = abs(peg1[0] - peg2[0])
            col_diff = abs(peg1[1] - peg2[1])
            
            # They can only capture if they're 2 spaces apart in one direction
            # and there's a blank space between them (but we know there are only 2 pegs)
            # Since there are only 2 pegs total, they cannot capture each other
            # because there's no peg to jump over
            return True
            
        # Also check if no valid moves remain
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.layout[row, col] == 'P':
                    # Check all possible jump directions
                    for dr, dc in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                        new_row, new_col = row + dr, col + dc
                        if (0 <= new_row < self.board.height and 
                            0 <= new_col < self.board.width and
                            self.board.layout[new_row, new_col] == '_'):
                            
                            # Check if there's a peg to jump over
                            jump_row, jump_col = row + dr//2, col + dc//2
                            if (0 <= jump_row < self.board.height and 
                                0 <= jump_col < self.board.width and
                                self.board.layout[jump_row, jump_col] == 'P'):
                                return False  # Valid move exists
        return True  # No valid moves
    
    def get_winner(self):
        peg_count = np.count_nonzero(self.board.layout == 'P')
        if peg_count == 2:
            return 0  # Player wins with 2 remaining pegs
        return None  # No winner (game lost or draw)
    
    def next_player(self):
        return 0  # Single player game
    
    def finish_message(self, winner):
        peg_count = np.count_nonzero(self.board.layout == 'P')
        if winner == 0:
            print(f"Congratulations! You won with {peg_count} pegs remaining in {self.moves_made} moves!")
        else:
            print(f"Game over! You finished with {peg_count} pegs remaining.")

if __name__ == '__main__':
    # Create the standard English peg solitaire board
    layout = """   
  PPP  
  PPP  
PPPPPPP
PP_PPPP
PPPPPPP
  PPP  
  PPP   
"""
    board = Board((7, 7), layout)
    mygame = PegSolitaire(board)
    mygame.game_loop()