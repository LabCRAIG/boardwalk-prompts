from game import Game, Board, is_placement, get_move_elements
import numpy as np

class Tangerine(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Player 1 starts (H pieces)
        
    def initial_player(self):
        return 1
    
    def validate_move(self, move):
        if not super().validate_move(move):
            return False
            
        if not is_placement(move):
            return False
            
        piece, (row, col) = get_move_elements(move)
        piece_type = piece.upper()
        
        # Verify correct piece for current player
        if (self.current_player == 1 and piece_type != 'H') or \
           (self.current_player == 2 and piece_type != 'V'):
            return False
            
        # Check board boundaries
        if piece_type == 'H':
            if col + 1 >= self.board.width:
                return False
        elif piece_type == 'V':
            if row - 1 < 0:
                return False
                
        # Check if spaces are free
        if piece_type == 'H':
            return (self.board.layout[row, col] == '_' and 
                    self.board.layout[row, col + 1] == '_')
        else:  # V
            return (self.board.layout[row, col] == '_' and 
                    self.board.layout[row - 1, col] == '_')
    
    def perform_move(self, move):
        piece, (row, col) = get_move_elements(move)
        piece_type = piece.upper()
        
        if piece_type == 'H':
            self.board.place_piece(f"H {row},{col}")
            self.board.place_piece(f"H {row},{col+1}")
        else:  # V
            self.board.place_piece(f"V {row},{col}")
            self.board.place_piece(f"V {row-1},{col}")
    
    def game_finished(self):
        # Check if current player has any valid moves left
        piece_type = 'H' if self.current_player == 1 else 'V'
        
        for row in range(self.board.height):
            for col in range(self.board.width):
                test_move = f"{piece_type} {row},{col}"
                if self.validate_move(test_move):
                    return False
        return True
    
    def get_winner(self):
        # The winner is the other player if game is finished
        return 2 if self.current_player == 1 else 1
    
    def next_player(self):
        return 2 if self.current_player == 1 else 1
    
    def prompt_current_player(self):
        piece_type = 'H' if self.current_player == 1 else 'V'
        return input(f"Player {self.current_player} ({piece_type}), enter your move (e.g., 'H 2,3'): ")
    
    def finish_message(self, winner):
        print(f"\nPlayer {winner} wins! Player {self.current_player} has no valid moves.")

if __name__ == '__main__':
    # Initialize 6x6 blank board
    board = Board((6, 6))
    game = Tangerine(board)
    game.game_loop()
