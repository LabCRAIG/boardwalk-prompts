from game import Game, Board, is_movement, is_placement, get_move_elements
import numpy as np

class Saffron(Game):
    def __init__(self, board):
        super().__init__(board)
        self.current_player = 1  # Override initial player
        # Track positions of main pieces
        center = board.height // 2
        self.a_pos = (center-1, center-1)
        self.b_pos = (center, center)
        
    def prompt_current_player(self):
        """Override to provide player-specific prompts"""
        piece = 'A' if self.current_player == 1 else 'B'
        print(f"Player {self.current_player}'s turn ({piece})")
        return input("Enter move as 'row,col': ")
    
    def validate_move(self, move):
        """Verify the move is valid according to game rules"""
        if not super().validate_move(move):  # Basic coordinate validation
            return False
        
        if not is_movement(move):  # Saffron only uses movement, not placement
            return False
            
        (from_pos), (to_row, to_col) = get_move_elements(move)
        
        # Verify moving correct piece
        if self.current_player == 1:
            if from_pos != self.a_pos:
                print("You can only move your A piece!")
                return False
            opponent_piece = 'B'
        else:
            if from_pos != self.b_pos:
                print("You can only move your B piece!")
                return False
            opponent_piece = 'A'
            
        # Check orthogonal movement
        dx = abs(to_row - from_pos[0])
        dy = abs(to_col - from_pos[1])
        if not ((dx == 1 and dy == 0) or (dx == 0 and dy == 1)):
            print("Must move orthogonally (up/down/left/right)")
            return False
            
        # Check target space
        target = self.board.layout[to_row, to_col]
        if target == opponent_piece:
            print("Cannot move onto opponent's piece!")
            return False
            
        return True
    
    def perform_move(self, move):
        """Execute the move and update game state"""
        (from_row, from_col), (to_row, to_col) = get_move_elements(move)
        
        # Check for loss condition (moving onto marker)
        if self.board.layout[to_row, to_col] in ['a', 'b']:
            self.winner = 2 if self.current_player == 1 else 1
            return
            
        # Place marker at current position
        marker = 'a' if self.current_player == 1 else 'b'
        self.board.place_piece(f"{marker} {from_row},{from_col}")
        
        # Move the main piece
        piece = 'A' if self.current_player == 1 else 'B'
        self.board.move_piece(f"{from_row},{from_col} {to_row},{to_col}")
        self.board.place_piece(f"{piece} {to_row},{to_col}")
        
        # Update position trackers
        if self.current_player == 1:
            self.a_pos = (to_row, to_col)
        else:
            self.b_pos = (to_row, to_col)
    
    def game_finished(self):
        """Check if game has ended"""
        return hasattr(self, 'winner')
    
    def get_winner(self):
        """Return the winning player if game is over"""
        return getattr(self, 'winner', None)
    
    def next_player(self):
        """Alternate players"""
        return 2 if self.current_player == 1 else 1
    
    def finish_message(self, winner):
        """Custom end game message"""
        print(f"Player {winner} wins! Game over.")

if __name__ == '__main__':
    # Create initial board setup
    initial_layout = ""
    for i in range(8):
        row = ['_'] * 8
        if i == 3:
            row[3] = 'A'
        elif i == 4:
            row[4] = 'B'
        initial_layout += ''.join(row) + '\n'
    
    board = Board((8, 8), initial_layout.strip())
    game = Saffron(board)
    game.game_loop()
